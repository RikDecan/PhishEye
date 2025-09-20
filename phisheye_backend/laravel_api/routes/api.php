<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\PhishingController;

Route::post('/analyze-email', [PhishingController::class, 'analyzeEmail']);
// Route::post('/analyze-text', [PhishingController::class, 'analyzeText']);
Route::post('/predict', [PhishingController::class, 'analyzeText']);

Route::get('/health', [PhishingController::class, 'health']);