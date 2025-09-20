// pdfGenerator.js
// Voor PDF generatie heb je jsPDF nodig: npm install jspdf

import jsPDF from 'jspdf'

export default {
  name: 'pdfGenerator',
  
  /**
   * Genereert een PDF rapport van de phishing analyse resultaten
   * @param {Object} analysisResults - De analyse resultaten van de API
   * @param {string} originalText - De originele tekst die geanalyseerd werd (optioneel)
   */
  generateAnalysisReport(analysisResults, originalText = '') {
    try {
      // Nieuwe PDF instantie maken
      const doc = new jsPDF()
      
      // Layout constanten
      const margin = 20
      const pageWidth = 210 // A4 breedte
      const columnWidth = (pageWidth - 3 * margin) / 2 // Twee kolommen met tussenruimte
      const leftColumnX = margin
      const rightColumnX = margin + columnWidth + margin
      
      let leftY = 20
      let rightY = 20
      
      // Header over volle breedte
      doc.setFontSize(22)
      doc.setFont('helvetica', 'bold')
      doc.text('PhishEye Report', leftColumnX, leftY)
      leftY += 10
      
      // Datum en tijd
      doc.setFontSize(10)
      doc.setFont('helvetica', 'normal')
      const processedDate = new Date(analysisResults.metadata.processed_at).toLocaleString()
      doc.text(`Generated: ${processedDate}`, leftColumnX, leftY)
      leftY += 8
      
      // Lijn over volle breedte
      doc.line(leftColumnX, leftY, pageWidth - margin, leftY)
      leftY += 15
      rightY = leftY
      
      // === LINKER KOLOM ===
      
      // Executive Summary Box
      this.addColoredBox(doc, leftColumnX, leftY - 5, columnWidth, 45, [255, 255, 255])
      doc.setFontSize(16)
      doc.setFont('helvetica', 'bold')
      doc.text('Executive Summary', leftColumnX + 5, leftY + 5)
      leftY += 12
      
      const threatLevel = analysisResults.analysis.enhanced_metadata.threat_level || 'unknown'
      const isPhishing = analysisResults.analysis.label === 'phishing'
      
      doc.setFontSize(12)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(isPhishing ? 220 : 0, isPhishing ? 20 : 150, isPhishing ? 60 : 0)
      doc.text(`${isPhishing ? 'PHISHING DETECTED' : 'LEGITIMATE'}`, leftColumnX + 5, leftY)
      doc.setTextColor(0, 0, 0)
      leftY += 8
      
      doc.setFont('helvetica', 'normal')
      doc.text(`Threat Level: ${threatLevel.toUpperCase()}`, leftColumnX + 5, leftY)
      leftY += 6
      doc.text(`Confidence: ${(analysisResults.analysis.confidence * 100).toFixed(1)}%`, leftColumnX + 5, leftY)
      leftY += 15
      
      // Risk Scores Section - Linker kolom
      this.addSectionHeader(doc, 'Risk Assessment Scores', leftColumnX, leftY)
      leftY += 10
      
      const scores = [
        { label: 'Overall Risk', value: (analysisResults.analysis.threat_analysis.overall_risk_score * 100).toFixed(1) + '%', color: this.getScoreColor(analysisResults.analysis.threat_analysis.overall_risk_score) },
        { label: 'Phishing Score', value: (analysisResults.analysis.score * 100).toFixed(1) + '%', color: this.getScoreColor(analysisResults.analysis.score) },
        { label: 'Urgency Score', value: (analysisResults.analysis.threat_analysis.urgency_score * 100).toFixed(1) + '%', color: this.getScoreColor(analysisResults.analysis.threat_analysis.urgency_score) },
        { label: 'Financial Risk', value: (analysisResults.analysis.threat_analysis.financial_risk * 100).toFixed(1) + '%', color: this.getScoreColor(analysisResults.analysis.threat_analysis.financial_risk) }
      ]
      
      scores.forEach(score => {
        doc.setFont('helvetica', 'normal')
        doc.setTextColor(0, 0, 0)
        doc.text(`${score.label}:`, leftColumnX + 5, leftY)
        doc.setFont('helvetica', 'bold')
        doc.setTextColor(score.color.r, score.color.g, score.color.b)
        doc.text(score.value, leftColumnX + 5 + 35, leftY)
        leftY += 7
      })
      doc.setTextColor(0, 0, 0)
      leftY += 10
      
      // Risk Factors - Linker kolom
      this.addSectionHeader(doc, 'Risk Factors', leftColumnX, leftY)
      leftY += 10
      
      const riskFactors = analysisResults.analysis.threat_analysis.risk_factors
      Object.entries(riskFactors).forEach(([key, value]) => {
        const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
        doc.setFont('helvetica', 'normal')
        doc.text(`${formattedKey}:`, leftColumnX + 5, leftY)
        doc.setFont('helvetica', 'bold')
        doc.text(`${value}`, leftColumnX + 5 + 55, leftY)
        leftY += 7
      })
      leftY += 10
      
      // === RECHTER KOLOM ===
      
      // Technical Details Box
      this.addColoredBox(doc, rightColumnX, rightY - 5, columnWidth, 35, [255, 250, 240])
      doc.setFontSize(16)
      doc.setFont('helvetica', 'bold')
      doc.text('Technical Details', rightColumnX + 5, rightY + 5)
      rightY += 12
      
      const technicalDetails = [
        { label: 'Classification', value: analysisResults.analysis.threat_analysis.technique_classification },
        { label: 'Processing Time', value: `${analysisResults.analysis.enhanced_metadata.processing_time_ms}ms` },
        { label: 'Model Used', value: 'XLM-RoBERTa' }
      ]
      
      doc.setFontSize(10)
      doc.setFont('helvetica', 'normal')
      technicalDetails.forEach(detail => {
        doc.text(`${detail.label}:`, rightColumnX + 5, rightY)
        const splitValue = doc.splitTextToSize(detail.value, columnWidth - 30)
        doc.text(splitValue, rightColumnX + 5, rightY + 4)
        rightY += 8
      })
      rightY += 10
      
      // Text Statistics
      this.addSectionHeader(doc, 'Text Analysis', rightColumnX, rightY)
      rightY += 10
      
      const textStats = [
        { label: 'Word Count', value: analysisResults.analysis.text_stats.word_count },
        { label: 'Sentences', value: analysisResults.analysis.text_stats.sentence_count },
        { label: 'Characters', value: analysisResults.analysis.text_stats.character_count },
        { label: 'URLs Found', value: analysisResults.analysis.text_stats.url_count }
      ]
      
      textStats.forEach(stat => {
        doc.text(`${stat.label}: ${stat.value}`, rightColumnX + 5, rightY)
        rightY += 7
      })
      rightY += 10
      
      // Threat Keywords - Rechter kolom
      if (analysisResults.analysis.threat_analysis.threat_keywords.length > 0) {
        this.addSectionHeader(doc, 'Threat Keywords', rightColumnX, rightY)
        rightY += 10
        
        // Keywords in een box
        const keywordHeight = Math.min(analysisResults.analysis.threat_analysis.threat_keywords.length * 6 + 10, 50)
        this.addColoredBox(doc, rightColumnX, rightY - 5, columnWidth, keywordHeight, [255, 255, 255])
        
        analysisResults.analysis.threat_analysis.threat_keywords.forEach(keyword => {
          doc.setFont('helvetica', 'normal')
          doc.setFontSize(9)
          doc.setTextColor(180, 20, 20)
          doc.text(`• ${keyword}`, rightColumnX + 5, rightY)
          rightY += 6
        })
        doc.setTextColor(0, 0, 0)
        rightY += 10
      }
      
      // Suspicious URLs (als ze er zijn)
      if (analysisResults.analysis.threat_analysis.suspicious_urls.length > 0) {
        // Check of we een nieuwe pagina nodig hebben
        if (rightY > 200) {
          doc.addPage()
          rightY = 20
        }
        
        this.addSectionHeader(doc, 'Suspicious URLs', rightColumnX, rightY)
        rightY += 10
        
        analysisResults.analysis.threat_analysis.suspicious_urls.forEach(url => {
          doc.setTextColor(255, 0, 0)
          doc.setFontSize(9)
          const splitUrl = doc.splitTextToSize(url, columnWidth - 10)
          doc.text(splitUrl, rightColumnX + 5, rightY)
          rightY += splitUrl.length * 5 + 3
        })
        doc.setTextColor(0, 0, 0)
        rightY += 10
      }
      
      // Bepaal de laagste Y positie voor de volgende sectie
      let nextY = Math.max(leftY, rightY) + 15
      
      // Threat Summary over volle breedte
      if (analysisResults.analysis.threat_summary.length > 0) {
        if (nextY > 220) {
          doc.addPage()
          nextY = 20
        }
        
        doc.setFontSize(16)
        doc.setFont('helvetica', 'bold')
        doc.text('Threat Analysis Summary', leftColumnX, nextY)
        nextY += 10
        
        // Summary box over volle breedte
        const summaryHeight = analysisResults.analysis.threat_summary.length * 8 + 10
        this.addColoredBox(doc, leftColumnX, nextY - 5, pageWidth - 2 * margin, summaryHeight, [255, 255, 255])
        
        doc.setFontSize(11)
        doc.setFont('helvetica', 'normal')
        analysisResults.analysis.threat_summary.forEach((summary, index) => {
          const bulletPoint = `${index + 1}. ${summary}`
          const splitSummary = doc.splitTextToSize(bulletPoint, pageWidth - 2 * margin - 10)
          doc.text(splitSummary, leftColumnX + 5, nextY)
          nextY += splitSummary.length * 6 + 3
        })
        nextY += 15
      }
      
      // Originele tekst (indien beschikbaar)
      if (originalText && originalText.trim()) {
        if (nextY > 200) {
          doc.addPage()
          nextY = 20
        }
        
        doc.setFontSize(16)
        doc.setFont('helvetica', 'bold')
        doc.text('Original Analyzed Content', leftColumnX, nextY)
        nextY += 10
        
        doc.setFontSize(10)
        doc.setFont('helvetica', 'italic')
        const splitText = doc.splitTextToSize(originalText, pageWidth - 2 * margin - 10)
        this.addColoredBox(doc, leftColumnX, nextY - 5, pageWidth - 2 * margin, splitText.length * 5 + 10, [248, 248, 248])
        doc.text(splitText, leftColumnX + 5, nextY)
      }
      
      // Footer op elke pagina
      const pageCount = doc.internal.getNumberOfPages()
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i)
        doc.setFontSize(8)
        doc.setFont('helvetica', 'normal')
        doc.setTextColor(100, 100, 100)
        doc.text(`PhishEye Analysis Report - Page ${i} of ${pageCount}`, leftColumnX, 285)
        doc.text(`Report ID: ${analysisResults.analysis.enhanced_metadata.email_hash || 'N/A'}`, leftColumnX, 290)
        // Datum rechts
        doc.text(new Date().toLocaleDateString(), pageWidth - margin - 30, 285)
      }
      
      // PDF downloaden met betere naam
      const date = new Date().toISOString().split('T')[0]
      const time = new Date().toTimeString().split(' ')[0].replace(/:/g, '-')
      const fileName = `PhishEye_Report_${threatLevel}_${date}_${time}.pdf`
      doc.save(fileName)
      
      return {
        success: true,
        fileName: fileName,
        message: 'PDF report generated successfully'
      }
      
    } catch (error) {
      console.error('Error generating PDF:', error)
      return {
        success: false,
        error: error.message,
        message: 'Failed to generate PDF report'
      }
    }
  },
  
  /**
   * Helper functie voor sectie headers
   */
  addSectionHeader(doc, title, x, y) {
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.text(title, x, y)
    doc.setFontSize(12)
    doc.setFont('helvetica', 'normal')
  },
  
  /**
   * Helper functie voor gekleurde achtergrond boxes
   */
  addColoredBox(doc, x, y, width, height, color = [0, 0, 0]) {
    doc.setFillColor(color[0], color[0], color[0])
    doc.rect(x, y, width, height, 'F')
  },
  
  /**
   * Helper functie voor score kleuren
   */
  getScoreColor(score) {
    if (score >= 0.7) return { r: 220, g: 20, b: 60 }   // Rood
    if (score >= 0.5) return { r: 255, g: 140, b: 0 }   // Oranje  
    if (score >= 0.3) return { r: 255, g: 193, b: 7 }   // Geel
    return { r: 34, g: 197, b: 94 }                     // Groen
  },
  
  /**
   * Genereert een simplified versie van het rapport
   */
  generateQuickReport(analysisResults) {
    try {
      const doc = new jsPDF()
      
      // Quick header
      doc.setFontSize(18)
      doc.setFont('helvetica', 'bold')
      doc.text('PhishEye Quick Analysis', 20, 30)
      
      // Main result
      doc.setFontSize(14)
      const isPhishing = analysisResults.analysis.label === 'phishing'
      const resultText = isPhishing ? 'PHISHING DETECTED' : 'EMAIL IS SAFE'
      const threatLevel = analysisResults.analysis.enhanced_metadata.threat_level.toUpperCase()
      
      doc.text(`Result: ${resultText}`, 20, 50)
      doc.text(`Threat Level: ${threatLevel}`, 20, 65)
      doc.text(`Confidence: ${(analysisResults.analysis.confidence * 100).toFixed(1)}%`, 20, 80)
      
      // Key metrics
      doc.setFontSize(12)
      doc.text('Key Risk Scores:', 20, 105)
      doc.text(`Overall Risk: ${(analysisResults.analysis.threat_analysis.overall_risk_score * 100).toFixed(1)}%`, 25, 120)
      doc.text(`Financial Risk: ${(analysisResults.analysis.threat_analysis.financial_risk * 100).toFixed(1)}%`, 25, 135)
      
      // Generated timestamp
      doc.setFontSize(10)
      doc.text(`Generated: ${new Date().toLocaleString()}`, 20, 270)
      
      const fileName = `phisheye-quick-${Date.now()}.pdf`
      doc.save(fileName)
      
      return {
        success: true,
        fileName: fileName,
        message: 'Quick PDF report generated successfully'
      }
      
    } catch (error) {
      console.error('Error generating quick PDF:', error)
      return {
        success: false,
        error: error.message,
        message: 'Failed to generate quick PDF report'
      }
    }
  }
}