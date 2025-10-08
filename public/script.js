// Function to apply justified text with centered last line to all paragraphs.
function applyJustifiedTextCenteringToAllParagraphs() {
    const paragraphs = document.querySelectorAll('main');
    paragraphs.forEach(paragraph => {
        paragraph.style.textAlign = 'justify';
    });
};

// apply the styles when the url is loaded
window.addEventListener('load', applyJustifiedTextCenteringToAllParagraphs);
