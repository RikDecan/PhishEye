<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Exception;

class PhishingDetectionService
{
    private $apiUrl;
    private $timeout;

    public function __construct()
    {
        $this->apiUrl = config('services.phishing_api.url', 'http://127.0.0.1:8000');
        $this->timeout = config('services.phishing_api.timeout', 30);
    }

    /**
     * Analyze single email for phishing with enhanced threat intelligence
     */
    public function analyzeEmail(string $emailText): array
    {
        try {
            $response = Http::timeout($this->timeout)
                ->post($this->apiUrl . '/predict', [
                    'text' => $emailText,
                    'max_length' => 512
                ]);

            if ($response->successful()) {
                $data = $response->json();
                
                // Enhance the response with additional processing
                return $this->enhanceAnalysisData($data, $emailText);
            }

            throw new Exception('API request failed: ' . $response->status());

        } catch (Exception $e) {
            Log::error('Phishing detection failed', [
                'error' => $e->getMessage(),
                'email_preview' => substr($emailText, 0, 100)
            ]);

            return [
                'label' => 'error',
                'score' => 0.0,
                'confidence' => 0.0,
                'error' => $e->getMessage(),
                'threat_analysis' => $this->getDefaultThreatAnalysis(),
                'text_stats' => $this->getBasicTextStats($emailText)
            ];
        }
    }

    /**
     * Enhance analysis data with additional Laravel-side processing
     */
    private function enhanceAnalysisData(array $data, string $emailText): array
    {
        // Add Laravel-specific enhancements
        $data['enhanced_metadata'] = [
            'analysis_timestamp' => now()->toISOString(),
            'processing_time_ms' => round(microtime(true) * 1000) - round(microtime(true) * 1000),
            'email_hash' => hash('sha256', $emailText),
            'threat_level' => $this->calculateThreatLevel($data),
            'risk_category' => $this->categorizeRisk($data)
        ];

        // Add human-readable threat summary
        $data['threat_summary'] = $this->generateThreatSummary($data);

        return $data;
    }

    /**
     * Calculate overall threat level
     */
    private function calculateThreatLevel(array $data): string
    {
        if (!isset($data['threat_analysis'])) {
            return 'unknown';
        }

        $threatAnalysis = $data['threat_analysis'];
        $overallRisk = $threatAnalysis['overall_risk_score'] ?? 0;
        $confidence = $data['confidence'] ?? 0;

        // Combine model confidence with threat analysis
        $combinedScore = ($confidence + $overallRisk) / 2;

        if ($combinedScore >= 0.8) return 'critical';
        if ($combinedScore >= 0.6) return 'high';
        if ($combinedScore >= 0.4) return 'medium';
        if ($combinedScore >= 0.2) return 'low';
        return 'minimal';
    }

    /**
     * Categorize risk type
     */
    private function categorizeRisk(array $data): string
    {
        if ($data['label'] === 'legitimate') {
            return 'safe';
        }

        $threatAnalysis = $data['threat_analysis'] ?? [];
        $technique = $threatAnalysis['technique_classification'] ?? 'unknown';

        return strtolower(str_replace(' ', '_', $technique));
    }

    /**
     * Generate human-readable threat summary
     */
    private function generateThreatSummary(array $data): array
    {
        $summary = [];
        $threatAnalysis = $data['threat_analysis'] ?? [];

        if ($data['label'] === 'legitimate') {
            $summary[] = "This email appears to be legitimate with low risk indicators.";
        } else {
            $summary[] = "This email shows characteristics of a phishing attempt.";
        }

        // Add specific threat insights
        if ($threatAnalysis['urgency_score'] ?? 0 > 0.5) {
            $summary[] = "Contains urgent language designed to pressure recipients.";
        }

        if ($threatAnalysis['financial_risk'] ?? 0 > 0.5) {
            $summary[] = "Mentions financial or account-related threats.";
        }

        if (!empty($threatAnalysis['suspicious_urls'] ?? [])) {
            $urlCount = count($threatAnalysis['suspicious_urls']);
            $summary[] = "Contains {$urlCount} suspicious URL(s) that should be avoided.";
        }

        if (!empty($threatAnalysis['impersonation_indicators'] ?? [])) {
            $summary[] = "Attempts to impersonate authority figures or organizations.";
        }

        return $summary;
    }

    /**
     * Batch analyze multiple emails
     */
    public function batchAnalyze(array $emails): array
    {
        $emailRequests = array_map(function($email) {
            return [
                'text' => $email,
                'max_length' => 512
            ];
        }, $emails);

        try {
            $response = Http::timeout($this->timeout * 2)
                ->post($this->apiUrl . '/batch_predict', $emailRequests);

            if ($response->successful()) {
                $data = $response->json();
                
                // Enhance each prediction in batch
                if (isset($data['predictions'])) {
                    foreach ($data['predictions'] as $index => $prediction) {
                        if (!isset($prediction['error'])) {
                            $data['predictions'][$index] = $this->enhanceAnalysisData(
                                $prediction, 
                                $emails[$index] ?? ''
                            );
                        }
                    }
                }
                
                return $data;
            }

            throw new Exception('Batch API request failed: ' . $response->status());

        } catch (Exception $e) {
            Log::error('Batch phishing detection failed', [
                'error' => $e->getMessage(),
                'email_count' => count($emails)
            ]);

            return [
                'predictions' => [],
                'total' => 0,
                'error' => $e->getMessage()
            ];
        }
    }

    /**
     * Check if the API is healthy
     */
    public function healthCheck(): bool
    {
        try {
            $response = Http::timeout(5)
                ->get($this->apiUrl . '/health');

            return $response->successful() && 
                   $response->json('model_loaded', false);

        } catch (Exception $e) {
            Log::warning('Phishing API health check failed', [
                'error' => $e->getMessage()
            ]);
            return false;
        }
    }

    /**
     * Extract and clean email text for analysis
     */
    public function preprocessEmail(string $rawEmail): string
    {
        // Remove excessive whitespace
        $cleaned = preg_replace('/\s+/', ' ', $rawEmail);
        
        // Remove email headers (basic cleanup)
        $cleaned = preg_replace('/^(From|To|Subject|Date|Message-ID):.*$/m', '', $cleaned);
        
        // Remove HTML tags if present
        $cleaned = strip_tags($cleaned);
        
        // Trim and limit length for model
        return trim(substr($cleaned, 0, 5000));
    }

    /**
     * Get default threat analysis for error cases
     */
    private function getDefaultThreatAnalysis(): array
    {
        return [
            'urgency_score' => 0.0,
            'financial_risk' => 0.0,
            'suspicious_urls' => [],
            'threat_keywords' => [],
            'impersonation_indicators' => [],
            'risk_factors' => [
                'urgency_indicators' => 0,
                'financial_threats' => 0,
                'authority_impersonation' => 0,
                'suspicious_urls' => 0,
                'grammar_errors' => 0,
                'excessive_punctuation' => 0
            ],
            'technique_classification' => 'unknown',
            'overall_risk_score' => 0.0
        ];
    }

    /**
     * Get basic text statistics
     */
    private function getBasicTextStats(string $text): array
    {
        return [
            'character_count' => strlen($text),
            'word_count' => str_word_count($text),
            'sentence_count' => preg_match_all('/[.!?]+/', $text),
            'url_count' => preg_match_all('/https?:\/\/\S+/', $text)
        ];
    }
}