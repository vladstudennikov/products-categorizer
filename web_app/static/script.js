document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const exportBtn = document.getElementById('export-btn');
    const loadingSection = document.getElementById('loading');
    const resultsSection = document.getElementById('results');
    const reportContent = document.getElementById('report-content');

    let currentReport = "";

    analyzeBtn.addEventListener('click', async () => {
        // Reset state
        analyzeBtn.disabled = true;
        exportBtn.disabled = true;
        loadingSection.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        reportContent.innerHTML = "";

        try {
            const response = await fetch('/api/analyze');
            if (!response.ok) {
                throw new Error('Failed to generate analysis. Check console for details.');
            }

            const data = await response.json();
            currentReport = data.report;

            // Render Markdown
            reportContent.innerHTML = marked.parse(currentReport);
            
            // Show results
            loadingSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');
            exportBtn.disabled = false;
        } catch (error) {
            console.error('Error:', error);
            alert('Error: ' + error.message);
            loadingSection.classList.add('hidden');
        } finally {
            analyzeBtn.disabled = false;
        }
    });

    exportBtn.addEventListener('click', () => {
        if (!currentReport) return;

        const blob = new Blob([currentReport], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        
        const timestamp = new Date().toISOString().split('T')[0];
        a.href = url;
        a.download = `Strategic_Analysis_${timestamp}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});
