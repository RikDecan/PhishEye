#!/usr/bin/env python3
"""
Fine-tuning XLM-RoBERTa for Phishing Detection
Script optimized for RunPod Linux server with RTX 3090
"""

import os
import pandas as pd
import torch
from datasets import Dataset, DatasetDict
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
from pathlib import Path


def setup_directories():
    """Setup and create necessary directories"""
    base_dir = Path("/workspace")

    dirs = {
        'dataset_dir': base_dir / "datasets",
        'output_dir': base_dir / "output",
        'scripts_dir': base_dir / "scripts",
        'libraries_dir': base_dir / "libraries"
    }

    # Create output directory if it doesn't exist
    dirs['output_dir'].mkdir(exist_ok=True)

    # Create subdirectories in output
    (dirs['output_dir'] / "model").mkdir(exist_ok=True)
    (dirs['output_dir'] / "results").mkdir(exist_ok=True)
    (dirs['output_dir'] / "logs").mkdir(exist_ok=True)

    return dirs


def check_gpu_specs():
    """Check GPU specifications and optimize settings accordingly"""
    if not torch.cuda.is_available():
        print("CUDA not available! Running on CPU.")
        return False, {}

    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9

    print(f"GPU: {gpu_name}")
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Available GPU memory: {gpu_memory:.1f} GB")

    # Optimized settings for stable training
    gpu_config = {
        'batch_size': 32,  # Can handle larger batches with RTX 3090
        'eval_batch_size': 64,  # Larger eval batches for speed
        'gradient_accumulation_steps': 1,
        'max_length': 512,
        'fp16': False,  # Disabled for stability
        'dataloader_num_workers': 2
    }

    if "3090" in gpu_name:
        print("Detected RTX 3090 - Using optimized settings for high-end GPU")
    else:
        print("Using conservative GPU settings")

    return True, gpu_config


def load_and_prepare_dataset(csv_path):
    """Load CSV and prepare dataset for training with memory optimization"""
    print(f"Loading dataset from: {csv_path}")

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at: {csv_path}")

    # Load CSV in chunks if it's very large
    try:
        df = pd.read_csv(csv_path)
    except MemoryError:
        print("Dataset too large for memory, loading in chunks...")
        chunks = []
        for chunk in pd.read_csv(csv_path, chunksize=10000):
            chunks.append(chunk)
        df = pd.concat(chunks, ignore_index=True)
        del chunks  # Free memory

    # Basic data validation
    print(f"Dataset shape: {df.shape}")
    print(f"Label distribution:\n{df['label'].value_counts()}")

    # Check for missing values
    if df.isnull().sum().any():
        print("Warning: Found missing values, dropping rows with NaN")
        df = df.dropna()

    # Ensure we have the required columns
    required_columns = ['body', 'label']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Memory optimization: convert to categorical if possible
    if df['label'].dtype == 'object':
        df['label'] = df['label'].astype('category').cat.codes

    # Split into train/test (90/10)
    train_df, test_df = train_test_split(
        df,
        test_size=0.1,
        random_state=42,
        stratify=df['label']
    )

    print(f"Train size: {len(train_df)}, Test size: {len(test_df)}")

    # Convert to Hugging Face Dataset format with memory optimization
    train_dataset = Dataset.from_pandas(train_df, preserve_index=False)
    test_dataset = Dataset.from_pandas(test_df, preserve_index=False)

    # Clear DataFrames from memory
    del df, train_df, test_df

    dataset_dict = DatasetDict({
        'train': train_dataset,
        'test': test_dataset
    })

    return dataset_dict


def tokenize_function(examples, tokenizer, max_length=512):
    """Tokenize the email body text"""
    return tokenizer(
        examples['body'],
        truncation=True,
        padding=False,  # We'll pad dynamically in the data collator
        max_length=max_length,
        return_tensors=None
    )


def compute_metrics(eval_pred):
    """Compute metrics for evaluation with better error handling"""
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)

    # Handle case where predictions are all one class
    try:
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, predictions, average='binary', zero_division=0
        )
        accuracy = accuracy_score(labels, predictions)

        # Debug print for first few evaluations
        print(f"Eval - Accuracy: {accuracy:.4f}, F1: {f1:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}")

        return {
            'accuracy': accuracy,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }
    except Exception as e:
        print(f"Error in compute_metrics: {e}")
        return {
            'accuracy': 0.0,
            'f1': 0.0,
            'precision': 0.0,
            'recall': 0.0
        }


def main():
    # Set environment variable to avoid tokenizer warnings
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    print("=" * 60)
    print("Fine-tuning XLM-RoBERTa for Phishing Detection")
    print("Optimized for RunPod Linux Server")
    print("=" * 60)

    # Setup directories
    dirs = setup_directories()

    # Configuration
    MODEL_NAME = "xlm-roberta-base"  # Using base model for better compatibility
    CSV_PATH = dirs['dataset_dir'] / "final_dataset.csv"
    MODEL_OUTPUT_DIR = dirs['output_dir'] / "model"
    RESULTS_DIR = dirs['output_dir'] / "results"
    LOGS_DIR = dirs['output_dir'] / "logs"

    print(f"Dataset path: {CSV_PATH}")
    print(f"Model output: {MODEL_OUTPUT_DIR}")
    print(f"Results output: {RESULTS_DIR}")

    # Check GPU and get optimized settings
    cuda_available, gpu_config = check_gpu_specs()

    if not cuda_available:
        print("WARNING: CUDA not available. Training will be very slow on CPU.")
        # CPU fallback settings
        gpu_config = {
            'batch_size': 8,
            'eval_batch_size': 16,
            'gradient_accumulation_steps': 4,
            'max_length': 256,
            'fp16': False,
            'dataloader_num_workers': 1
        }

    # Load dataset
    dataset = load_and_prepare_dataset(CSV_PATH)

    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Add padding token if it doesn't exist
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Tokenize datasets with memory optimization
    print("Tokenizing datasets with memory optimization...")
    tokenized_dataset = dataset.map(
        lambda examples: tokenize_function(examples, tokenizer, gpu_config['max_length']),
        batched=True,
        batch_size=1000,  # Process in smaller batches to reduce memory usage
        remove_columns=['body'],  # Remove original text column
        num_proc=1,  # Use single process to avoid memory multiplication
        load_from_cache_file=True,  # Cache results to disk
        desc="Tokenizing"  # Progress bar description
    )

    # Rename label column to labels (required by Trainer)
    tokenized_dataset = tokenized_dataset.rename_column("label", "labels")

    # Check for label distribution and potential issues
    print("Checking label distribution in tokenized dataset...")
    train_labels = tokenized_dataset["train"]["labels"]
    test_labels = tokenized_dataset["test"]["labels"]

    print(f"Train label distribution: {np.bincount(train_labels)}")
    print(f"Test label distribution: {np.bincount(test_labels)}")

    # Ensure labels are properly formatted
    if max(train_labels) > 1 or min(train_labels) < 0:
        print("ERROR: Labels should be 0 or 1 only!")
        print(f"Found labels in range: {min(train_labels)} to {max(train_labels)}")
        return

    # Load model with device specification for compatibility
    print("Loading model...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
        id2label={0: "legitimate", 1: "phishing"},
        label2id={"legitimate": 0, "phishing": 1},
        torch_dtype=torch.float32,  # Use FP32 for stability
        device_map="auto" if cuda_available else None
    )

    # Move model to device if device_map wasn't used
    if not cuda_available:
        model = model.to(device)

    # Data collator for dynamic padding
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # Training arguments optimized for stability
    training_args = TrainingArguments(
        output_dir=str(RESULTS_DIR),
        num_train_epochs=3,
        per_device_train_batch_size=gpu_config['batch_size'],
        per_device_eval_batch_size=gpu_config['eval_batch_size'],
        gradient_accumulation_steps=gpu_config['gradient_accumulation_steps'],
        warmup_steps=500,
        weight_decay=0.01,
        learning_rate=1e-5,  # Conservative learning rate
        logging_dir=str(LOGS_DIR),
        logging_steps=100,
        evaluation_strategy="steps",
        eval_steps=2000,  # Less frequent evaluation
        save_strategy="steps",
        save_steps=2000,  # Match eval_steps
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        fp16=False,  # Disabled for stability
        bf16=True if torch.cuda.is_bf16_supported() else False,
        dataloader_pin_memory=True,
        dataloader_num_workers=gpu_config['dataloader_num_workers'],
        remove_unused_columns=False,
        report_to=None,
        save_total_limit=3,
        prediction_loss_only=False,
        seed=42,
        data_seed=42,
        group_by_length=True,
        ddp_find_unused_parameters=False,
        max_grad_norm=1.0,
    )

    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    # Start training
    print("\n" + "=" * 50)
    print("STARTING TRAINING")
    print("=" * 50)
    print(f"Training samples: {len(tokenized_dataset['train'])}")
    print(f"Validation samples: {len(tokenized_dataset['test'])}")
    print(f"Batch size: {gpu_config['batch_size']}")
    print(f"Effective batch size: {gpu_config['batch_size'] * gpu_config['gradient_accumulation_steps']}")
    print(
        f"Total training steps: {len(tokenized_dataset['train']) // (gpu_config['batch_size'] * gpu_config['gradient_accumulation_steps']) * 3}")

    try:
        trainer.train()
    except RuntimeError as e:
        if "out of memory" in str(e).lower():
            print("\n" + "=" * 50)
            print("GPU OUT OF MEMORY ERROR!")
            print("=" * 50)
            print("Try reducing these parameters:")
            print(f"- Current batch_size: {gpu_config['batch_size']} -> try 8")
            print(f"- Current max_length: {gpu_config['max_length']} -> try 256")
            print("- Or increase gradient_accumulation_steps to 2 or 4")
            print("=" * 50)
        raise e

    # Evaluate on test set
    print("\n" + "=" * 50)
    print("FINAL EVALUATION")
    print("=" * 50)
    eval_results = trainer.evaluate()
    print("Final evaluation results:")
    for key, value in eval_results.items():
        print(f"  {key}: {value:.4f}")

    # Save the model and tokenizer
    print(f"\nSaving model to {MODEL_OUTPUT_DIR}...")
    trainer.save_model(MODEL_OUTPUT_DIR)
    tokenizer.save_pretrained(MODEL_OUTPUT_DIR)

    # Save training results and configuration
    results_file = RESULTS_DIR / "training_results.txt"
    config_file = RESULTS_DIR / "training_config.txt"

    with open(results_file, "w") as f:
        f.write("Fine-tuning XLM-RoBERTa for Phishing Detection\n")
        f.write("=" * 50 + "\n")
        f.write(f"Model: {MODEL_NAME}\n")
        f.write(f"GPU: {torch.cuda.get_device_name(0) if cuda_available else 'CPU'}\n")
        f.write(f"Dataset: {CSV_PATH}\n")
        f.write(f"Training samples: {len(tokenized_dataset['train'])}\n")
        f.write(f"Test samples: {len(tokenized_dataset['test'])}\n\n")

        f.write("Training Configuration:\n")
        f.write("-" * 25 + "\n")
        for key, value in gpu_config.items():
            f.write(f"{key}: {value}\n")
        f.write("\n")

        f.write("Final Evaluation Results:\n")
        f.write("-" * 28 + "\n")
        for key, value in eval_results.items():
            f.write(f"{key}: {value:.4f}\n")

    # Save detailed configuration
    with open(config_file, "w") as f:
        f.write("Training Arguments:\n")
        f.write("=" * 20 + "\n")
        for key, value in training_args.__dict__.items():
            f.write(f"{key}: {value}\n")

    print("\n" + "=" * 60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Model saved to: {MODEL_OUTPUT_DIR}")
    print(f"Results saved to: {RESULTS_DIR}")
    print(f"Logs saved to: {LOGS_DIR}")
    print("\nTo use the model for inference:")
    print("```python")
    print("from transformers import pipeline")
    print(f"classifier = pipeline('text-classification', model='{MODEL_OUTPUT_DIR}')")
    print("result = classifier('Your email text here')")
    print("```")


if __name__ == "__main__":
    # Check if required packages are available
    print("Checking dependencies...")
    try:
        import transformers
        import datasets
        import torch
        import sklearn

        print(f"✓ Transformers version: {transformers.__version__}")
        print(f"✓ PyTorch version: {torch.__version__}")
        print(f"✓ CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"✓ CUDA version: {torch.version.cuda}")
        print("✓ All dependencies satisfied\n")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install required packages:")
        print("pip install transformers datasets torch scikit-learn pandas")
        exit(1)

    main()