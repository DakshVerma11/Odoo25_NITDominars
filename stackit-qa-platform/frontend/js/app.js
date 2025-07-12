// Sample data
const sampleQuestions = [
    {
        id: 1,
        title: "How to implement machine learning in React with TensorFlow.js",
        excerpt: "I'm building a React application that needs to classify images using machine learning. What's the best approach to integrate TensorFlow.js for real-time inference?",
        votes: 12,
        answers: 3,
        views: 156,
        tags: ["react", "tensorflow", "machine-learning", "javascript"],
        author: "DevMaster",
        time: "2 hours ago"
    },
    {
        id: 2,
        title: "Best practices for microservices architecture in Node.js",
        excerpt: "I'm designing a microservices architecture for a large-scale application. What are the key considerations for service communication, data consistency, and deployment strategies?",
        votes: 8,
        answers: 2,
        views: 89,
        tags: ["nodejs", "microservices", "architecture", "docker"],
        author: "CloudExpert",
        time: "4 hours ago"
    },
    {
        id: 3,
        title: "Optimizing PostgreSQL queries for large datasets",
        excerpt: "My application is dealing with millions of records and query performance is becoming an issue. What are the most effective indexing strategies and query optimization techniques?",
        votes: 15,
        answers: 5,
        views: 234,
        tags: ["postgresql", "database", "performance", "optimization"],
        author: "DBGuru",
        time: "6 hours ago"
    },
    {
        id: 4,
        title: "Implementing real-time chat with WebSockets and Redis",
        excerpt: "I need to build a scalable real-time chat application. How should I handle message persistence, user presence, and horizontal scaling with Redis and WebSockets?",
        votes: 6,
        answers: 1,
        views: 67,
        tags: ["websockets", "redis", "realtime", "chat"],
        author: "FullStackDev",
        time: "8 hours ago"
    },
    {
        id: 5,
        title: "Kubernetes deployment strategies for zero-downtime updates",
        excerpt: "What are the best practices for deploying applications to Kubernetes with zero downtime? I need to understand rolling updates, blue-green deployments, and canary releases.",
        votes: 9,
        answers: 2,
        views: 123,
        tags: ["kubernetes", "deployment", "devops", "ci-cd"],
        author: "K8sExpert",
        time: "12 hours ago"
    },
    {
        id: 6,
        title: "Advanced React patterns: Compound Components and Render Props",
        excerpt: "I'm looking to understand advanced React patterns for building reusable UI components. Can someone explain compound components and render props with practical examples?",
        votes: 4,
        answers: 1,
        views: 45,
        tags: ["react", "patterns", "components", "advanced"],
        author: "ReactNinja",
        time: "1 day ago"
    }
];

// Application state
let currentFilter = 'newest';
let currentPage = 1;
let questionsPerPage = 5;
let filteredQuestions = [...sampleQuestions];
let isLoggedIn = false;
let currentUser = null;

// Initialize application
document.addEventListener('DOMContentLoaded', function () {
    renderQuestions();
    renderPagination();
    setupEventListeners();
    animateOnScroll();
});

// Event listeners
function setupEventListeners() {
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            if (this.classList.contains('dropdown-toggle')) {
                toggleDropdown();
            } else {
                setFilter(this.dataset.filter);
            }
        });
    });

    // Dropdown items
    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', function () {
            setFilter(this.dataset.filter);
            closeDropdown();
        });
    });

    // Search input
    document.getElementById('searchInput').addEventListener('input', debounce(performSearch, 300));

    // Modal form submissions
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);

    // Close modals when clicking outside
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target.id);
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            document.getElementById('searchInput').focus();
        }
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

// Render functions
function renderQuestions() {
    const container = document.getElementById('questionsContainer');
    const startIndex = (currentPage - 1) * questionsPerPage;
    const endIndex = startIndex + questionsPerPage;
    const questionsToShow = filteredQuestions.slice(startIndex, endIndex);

    if (questionsToShow.length === 0) {
        container.innerHTML = `
                    <div style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.6);">
                        <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                        <h3>No questions found</h3>
                        <p>Try adjusting your search or filter criteria</p>
                    </div>
                `;
        return;
    }

    container.innerHTML = questionsToShow.map(question => `
                <div class="question-card" data-question-id="${question.id}">
                    <div class="question-content">
                        <div class="question-main">
                            <h3 class="question-title">
                                <a href="#" onclick="viewQuestion(${question.id})">${question.title}</a>
                            </h3>
                            <p class="question-excerpt">${question.excerpt}</p>
                            <div class="question-meta">
                                <div class="question-tags">
                                    ${question.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                                </div>
                                <div class="question-author">
                                    <span class="author-name">${question.author}</span>
                                    <span class="question-time">${question.time}</span>
                                </div>
                            </div>
                        </div>
                        <div class="question-stats">
                            <div class="stat">
                                <span class="stat-number">${question.votes}</span>
                                <span class="stat-label">votes</span>
                            </div>
                            <div class="stat">
                                <span class="stat-number">${question.answers}</span>
                                <span class="stat-label">answers</span>
                            </div>
                            <div class="stat">
                                <span class="stat-number">${question.views}</span>
                                <span class="stat-label">views</span>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');

    // Add animation to cards
    setTimeout(() => {
        document.querySelectorAll('.question-card').forEach((card, index) => {
            card.style.animation = `slideIn 0.5s ease ${index * 0.1}s both`;
        });
    }, 50);
}

function renderPagination() {
    const totalPages = Math.ceil(filteredQuestions.length / questionsPerPage);
    const pagination = document.getElementById('pagination');

    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let paginationHTML = '';

    // Previous button
    paginationHTML += `
                <button class="page-btn" onclick="goToPage(${currentPage - 1})" ${currentPage <= 1 ? 'disabled' : ''}>
                    <i class="fas fa-chevron-left"></i>
                </button>
            `;

    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            paginationHTML += `
                        <button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">
                            ${i}
                        </button>
                    `;
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            paginationHTML += `<span style="color: rgba(255,255,255,0.5); padding: 0 0.5rem;">...</span>`;
        }
    }

    // Next button
    paginationHTML += `
                <button class="page-btn" onclick="goToPage(${currentPage + 1})" ${currentPage >= totalPages ? 'disabled' : ''}>
                    <i class="fas fa-chevron-right"></i>
                </button>
            `;

    pagination.innerHTML = paginationHTML;
}

// Filter and search functions
function setFilter(filter) {
    currentFilter = filter;
    currentPage = 1;

    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-filter="${filter}"]`).classList.add('active');

    // Apply filter
    switch (filter) {
        case 'newest':
            filteredQuestions = [...sampleQuestions].sort((a, b) => new Date(b.time) - new Date(a.time));
            break;
        case 'unanswered':
            filteredQuestions = sampleQuestions.filter(q => q.answers === 0);
            break;
        case 'active':
            filteredQuestions = [...sampleQuestions].sort((a, b) => b.answers - a.answers);
            break;
        case 'votes':
            filteredQuestions = [...sampleQuestions].sort((a, b) => b.votes - a.votes);
            break;
        case 'views':
            filteredQuestions = [...sampleQuestions].sort((a, b) => b.views - a.views);
            break;
        default:
            filteredQuestions = [...sampleQuestions];
    }

    renderQuestions();
    renderPagination();
    showNotification(`Filtered by ${filter}`, 'success');
}

function performSearch() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();

    if (searchTerm.trim() === '') {
        filteredQuestions = [...sampleQuestions];
    } else {
        filteredQuestions = sampleQuestions.filter(question =>
            question.title.toLowerCase().includes(searchTerm) ||
            question.excerpt.toLowerCase().includes(searchTerm) ||
            question.tags.some(tag => tag.toLowerCase().includes(searchTerm))
        );
    }

    currentPage = 1;
    renderQuestions();
    renderPagination();

    if (searchTerm.trim() !== '') {
        showNotification(`Found ${filteredQuestions.length} results`, 'success');
    }
}

// Pagination
function goToPage(page) {
    if (typeof page === 'string') {
        if (page === 'next') page = currentPage + 1;
        if (page === 'prev') page = currentPage - 1;
    }

    const totalPages = Math.ceil(filteredQuestions.length / questionsPerPage);
    if (page < 1 || page > totalPages) return;

    currentPage = page;
    renderQuestions();
    renderPagination();

    // Smooth scroll to top
    document.querySelector('.questions-container').scrollIntoView({
        behavior: 'smooth'
    });
}

// Modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';

    // Focus first input
    setTimeout(() => {
        const firstInput = modal.querySelector('input');
        if (firstInput) firstInput.focus();
    }, 100);
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('show');
    });
    document.body.style.overflow = 'auto';
}

function switchModal(fromModal, toModal) {
    closeModal(fromModal);
    setTimeout(() => openModal(toModal), 300);
}

// Form handlers
function handleLogin(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const email = formData.get('email');
    const password = formData.get('password');

    // Simulate login
    if (email && password) {
        isLoggedIn = true;
        currentUser = { email, username: email.split('@')[0] };

        closeModal('loginModal');
        showNotification('Welcome back!', 'success');
        updateAuthState();
    }
}

function handleRegister(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const username = formData.get('username');
    const email = formData.get('email');
    const password = formData.get('password');

    // Simulate registration
    if (username && email && password) {
        isLoggedIn = true;
        currentUser = { email, username };

        closeModal('registerModal');
        showNotification('Account created successfully!', 'success');
        updateAuthState();
    }
}

function updateAuthState() {
    const headerActions = document.querySelector('.header-actions');
    if (isLoggedIn) {
        headerActions.innerHTML = `
                    <span style="color: var(--white); margin-right: 1rem;">Welcome, ${currentUser.username}!</span>
                    <button class="btn btn-secondary" onclick="logout()">
                        <i class="fas fa-sign-out-alt"></i> Logout
                    </button>
                `;
    }
}

function logout() {
    isLoggedIn = false;
    currentUser = null;
    location.reload();
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

function toggleDropdown() {
    const dropdown = document.getElementById('moreFilters');
    dropdown.classList.toggle('show');
}

function closeDropdown() {
    const dropdown = document.getElementById('moreFilters');
    dropdown.classList.remove('show');
}

// Question actions
function viewQuestion(id) {
    showNotification(`Viewing question ${id}`, 'success');
    // In a real app, this would navigate to the question page
}


    function askQuestion() {
        window.location.href = 'ask-question.html';
    }


// Animations
function animateOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideIn 0.6s ease both';
            }
        });
    });

    document.querySelectorAll('.question-card').forEach(card => {
        observer.observe(card);
    });
}

function viewQuestion(id) {
    const question = sampleQuestions.find(q => q.id === id);
    if (!question) return;

    // Hide questions list and pagination
    document.getElementById('questionsContainer').style.display = 'none';
    document.getElementById('pagination').style.display = 'none';

    // Show question detail view
    const detailView = document.getElementById('questionDetail');
    detailView.style.display = 'block';

    // Populate question content
    document.getElementById('questionContent').innerHTML = `
        <h2>${question.title}</h2>
        <p>${question.excerpt}</p>
        <div class="question-meta">
            <span><strong>Author:</strong> ${question.author}</span> |
            <span><strong>Votes:</strong> ${question.votes}</span> |
            <span><strong>Views:</strong> ${question.views}</span>
        </div>
        <div class="question-tags">
            ${question.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
        </div>
    `;

    // Populate mock answers
    const answersHTML = Array(question.answers).fill(0).map((_, i) => `
        <div class="answer-card">
            <p><strong>User${i + 1}</strong> answered:</p>
            <p>This is a sample answer to "${question.title}".</p>
        </div>
    `).join('');
    document.getElementById('answersContainer').innerHTML = answersHTML || "<p>No answers yet.</p>";
}

function closeDetailView() {
    document.getElementById('questionDetail').style.display = 'none';
    document.getElementById('questionsContainer').style.display = 'block';
    document.getElementById('pagination').style.display = 'flex';
}


// Add CSS animation keyframes
const style = document.createElement('style');
style.textContent = `
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
document.head.appendChild(style);

// Close dropdowns when clicking outside
document.addEventListener('click', function (e) {
    if (!e.target.closest('.filter-group')) {
        closeDropdown();
    }
});

// Add loading states
function showLoading(element) {
    element.innerHTML = '<div class="loading"></div>';
}

// Real-time features simulation
setInterval(() => {
    // Simulate real-time updates
    if (Math.random() > 0.95) {
        const randomQuestion = sampleQuestions[Math.floor(Math.random() * sampleQuestions.length)];
        randomQuestion.views += Math.floor(Math.random() * 5) + 1;

        if (currentFilter === 'newest' || currentFilter === 'views') {
            renderQuestions();
        }
    }
}, 5000);

// Performance optimization
function throttle(func, limit) {
    let inThrottle;
    return function () {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Add smooth scrolling for better UX
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});