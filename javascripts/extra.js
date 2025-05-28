// Custom JavaScript for Marvin documentation

document.addEventListener('DOMContentLoaded', function() {
    // Add copy button functionality enhancement
    const codeBlocks = document.querySelectorAll('pre > code');
    
    codeBlocks.forEach(block => {
        // Add language label to code blocks
        const lang = block.className.match(/language-(\w+)/);
        if (lang && lang[1]) {
            const label = document.createElement('div');
            label.className = 'code-language-label';
            label.textContent = lang[1].toUpperCase();
            block.parentElement.insertBefore(label, block);
        }
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});