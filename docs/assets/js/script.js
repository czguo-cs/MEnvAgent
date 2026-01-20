// ===================================
// Scroll to Top Button
// ===================================

const scrollTopBtn = document.getElementById('scrollTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollTopBtn.classList.add('show');
    } else {
        scrollTopBtn.classList.remove('show');
    }
});

scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// ===================================
// Copy Citation to Clipboard
// ===================================

function copyCitation() {
    const citationText = `@article{menvagent2026,
  title={MEnvAgent: Scalable Polyglot Environment Construction for Verifiable Software Engineering},
  author={TODO: Add authors from paper},
  year={2026}
}`;

    // Create a temporary textarea element
    const textarea = document.createElement('textarea');
    textarea.value = citationText;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);

    // Select and copy
    textarea.select();
    document.execCommand('copy');

    // Remove the textarea
    document.body.removeChild(textarea);

    // Update button text temporarily
    const copyBtn = document.querySelector('.copy-btn');
    const originalHTML = copyBtn.innerHTML;
    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
    copyBtn.style.background = '#10b981';

    setTimeout(() => {
        copyBtn.innerHTML = originalHTML;
        copyBtn.style.background = '';
    }, 2000);
}

// ===================================
// Code Snippet Copy Functionality
// ===================================

const addCopyButtonsToCodeSnippets = () => {
    const codeSnippets = document.querySelectorAll('.code-snippet');

    codeSnippets.forEach(snippet => {
        if (snippet.querySelector('.copy-code-btn')) return; // Already has button

        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-code-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.title = 'Copy code';
        copyBtn.style.cssText = 'position: absolute; top: 0.75rem; right: 0.75rem; background: var(--primary-color); color: white; border: none; padding: 0.4rem 0.75rem; border-radius: 0.375rem; cursor: pointer; font-size: 0.85rem;';

        copyBtn.addEventListener('click', () => {
            const code = snippet.querySelector('code').textContent;
            const textarea = document.createElement('textarea');
            textarea.value = code;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);

            copyBtn.innerHTML = '<i class="fas fa-check"></i>';
            copyBtn.style.background = '#10b981';

            setTimeout(() => {
                copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                copyBtn.style.background = 'var(--primary-color)';
            }, 2000);
        });

        snippet.style.position = 'relative';
        snippet.appendChild(copyBtn);
    });
};

document.addEventListener('DOMContentLoaded', addCopyButtonsToCodeSnippets);

// ===================================
// External Link Handler
// ===================================

document.addEventListener('DOMContentLoaded', () => {
    const externalLinks = document.querySelectorAll('a[href^="http"]');

    externalLinks.forEach(link => {
        if (!link.hasAttribute('target')) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
});
