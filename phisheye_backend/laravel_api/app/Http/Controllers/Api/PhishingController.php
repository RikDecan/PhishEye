<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\PhishingDetectionService;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class PhishingController extends Controller
{
    protected $phishingService;

    public function __construct(PhishingDetectionService $phishingService)
    {
        $this->phishingService = $phishingService;
    }

    /**
     * Analyze uploaded email file
     */
    public function analyzeEmail(Request $request): JsonResponse
    {
        $request->validate([
            'email_file' => 'required|file|max:10240', // 10MB max
        ]);

        try {
            // Extract email content (implement based on file type)
            $emailContent = $this->extractEmailContent($request->file('email_file'));
            
            // Preprocess
            $cleanedEmail = $this->phishingService->preprocessEmail($emailContent);
            
            // Analyze
            $result = $this->phishingService->analyzeEmail($cleanedEmail);
            
            return response()->json([
                'success' => true,
                'analysis' => $result,
                'metadata' => [
                    'file_name' => $request->file('email_file')->getClientOriginalName(),
                    'file_size' => $request->file('email_file')->getSize(),
                    'processed_at' => now()
                ]
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'error' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * Analyze text directly (for testing)
     */
    public function analyzeText(Request $request): JsonResponse
    {
        $request->validate([
            'text' => 'required|string|max:5000',
        ]);

        try {
            $result = $this->phishingService->analyzeEmail($request->text);
            
            return response()->json([
                'success' => true,
                'analysis' => $result,
                'metadata' => [
                    'text_length' => strlen($request->text),
                    'processed_at' => now()
                ]
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'error' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * Extract content from email files (.eml, .msg, etc.)
     */
    private function extractEmailContent($file): string
    {
        $extension = $file->getClientOriginalExtension();
        $content = file_get_contents($file->getPathname());

        switch (strtolower($extension)) {
            case 'eml':
                // Basic EML parsing - you might want to use a proper library
                return $this->parseEmlContent($content);
            
            case 'txt':
                return $content;
            
            default:
                // Fallback to raw content
                return $content;
        }
    }

    private function parseEmlContent(string $emlContent): string
    {
        // Split headers and body at first blank line
        $parts = preg_split('/\r?\n\r?\n/', $emlContent, 2);
        return isset($parts[1]) ? trim($parts[1]) : $emlContent;
    }

    /**
     * API health check
     */
    public function health(): JsonResponse
    {
        return response()->json([
            'laravel_api' => true,
            'phishing_model' => $this->phishingService->healthCheck(),
            'timestamp' => now()
        ]);
    }
}