document.addEventListener('DOMContentLoaded', function() {
    // Get all question items
    const questionItems = document.querySelectorAll('.question-item');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const submitButton = document.querySelector('button[type="submit"]');
    
    // Initialize variables
    let currentQuestion = 0;
    const totalQuestions = questionItems.length;
    
    // Initially hide all questions except the first one
    questionItems.forEach((item, index) => {
        if (index !== 0) {
            item.style.display = 'none';
        }
    });
    
    // Create navigation buttons if they don't exist
    if (!document.getElementById('prev-btn') && !document.getElementById('next-btn')) {
        const navButtons = document.createElement('div');
        navButtons.className = 'nav-buttons';
        
        const prevButton = document.createElement('button');
        prevButton.id = 'prev-btn';
        prevButton.type = 'button';
        prevButton.className = 'nav-button';
        prevButton.innerHTML = '&larr; Previous';
        prevButton.disabled = true;
        
        const nextButton = document.createElement('button');
        nextButton.id = 'next-btn';
        nextButton.type = 'button';
        nextButton.className = 'nav-button';
        nextButton.innerHTML = 'Next &rarr;';
        
        navButtons.appendChild(prevButton);
        navButtons.appendChild(nextButton);
        
        // Insert before the submit button container
        const buttonContainer = document.querySelector('.button-container');
        buttonContainer.parentNode.insertBefore(navButtons, buttonContainer);
    }
    
    // Update progress bar and buttons
    function updateProgress() {
        const percentage = ((currentQuestion + 1) / totalQuestions) * 100;
        progressBar.style.width = percentage + '%';
        progressText.textContent = `Question ${currentQuestion + 1} of ${totalQuestions}`;
        
        // Update button states
        document.getElementById('prev-btn').disabled = (currentQuestion === 0);
        document.getElementById('next-btn').disabled = (currentQuestion === totalQuestions - 1);
        
        // Only show submit button on last question
        if (currentQuestion === totalQuestions - 1) {
            submitButton.style.display = 'inline-block';
        } else {
            submitButton.style.display = 'none';
        }
    }
    
    // Show a specific question
    function showQuestion(index) {
        // Hide all questions
        questionItems.forEach(item => {
            item.style.display = 'none';
        });
        
        // Show the current question with fade-in effect
        questionItems[index].style.display = 'block';
        questionItems[index].classList.add('fade-in');
        
        // Remove animation class after animation completes
        setTimeout(() => {
            questionItems[index].classList.remove('fade-in');
        }, 500);
        
        currentQuestion = index;
        updateProgress();
    }
    
    // Event listeners for navigation buttons
    document.getElementById('next-btn').addEventListener('click', function() {
        if (currentQuestion < totalQuestions - 1) {
            showQuestion(currentQuestion + 1);
        }
    });
    
    document.getElementById('prev-btn').addEventListener('click', function() {
        if (currentQuestion > 0) {
            showQuestion(currentQuestion - 1);
        }
    });
    
    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowRight' && currentQuestion < totalQuestions - 1) {
            showQuestion(currentQuestion + 1);
        } else if (e.key === 'ArrowLeft' && currentQuestion > 0) {
            showQuestion(currentQuestion - 1);
        }
    });
    
    // Initialize the progress display
    updateProgress();
    
    // Add animation to checkboxes
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                this.parentElement.classList.add('selected');
            } else {
                this.parentElement.classList.remove('selected');
            }
        });
    });
});