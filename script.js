window.addEventListener('scroll', function() {
  var navbar = document.querySelector('.navbar');
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

function toggleMenu() {
  var navMenu = document.getElementById('navMenu');
  navMenu.classList.toggle('active');
}

function toggleSearch() {
  var searchBar = document.getElementById('searchBar');
  searchBar.classList.toggle('active');
}

function performSearch() {
  var searchInput = document.getElementById('searchInput');
  var query = searchInput.value;
  if (query) {
    alert('Searching for: ' + query);
  } else {
    alert('Please enter a search term');
  }
}

function handleGetStarted() {
  var emailInput = document.getElementById('emailInput');
  if (emailInput) {
    var email = emailInput.value;
    if (email && email.includes('@')) {
      window.location.href = 'signup.html';
    } else {
      alert('Please enter a valid email address.');
    }
  } else {
    window.location.href = 'signup.html';
  }
}

function toggleFAQ(element) {
  var answer = element.nextElementSibling;
  element.classList.toggle('active');
  answer.classList.toggle('show');
}

function openModal(title) {
  var modal = document.getElementById('movieModal');
  var modalTitle = document.getElementById('modalTitle');
  var modalImage = document.getElementById('modalImage');
  var modalDescription = document.getElementById('modalDescription');
  
  modalTitle.textContent = title;
  modalImage.src = 'https://via.placeholder.com/250x350/51/e50914?text=' + encodeURIComponent(title);
  modalDescription.textContent = 'Experience the amazing story of ' + title + '. This captivating content will keep you on the edge of your seat with its incredible plot twists and memorable characters.';
  
  modal.style.display = 'block';
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  var modal = document.getElementById('movieModal');
  modal.style.display = 'none';
  document.body.style.overflow = 'auto';
}

window.onclick = function(event) {
  var modal = document.getElementById('movieModal');
  if (event.target == modal) {
    closeModal();
  }
}

function addToList() {
  var modalTitle = document.getElementById('modalTitle').textContent;
  var myList = JSON.parse(localStorage.getItem('myList') || '[]');
  
  if (!myList.includes(modalTitle)) {
    myList.push(modalTitle);
    localStorage.setItem('myList', JSON.stringify(myList));
    alert(modalTitle + ' has been added to your list!');
  } else {
    alert(modalTitle + ' is already in your list!');
  }
}

function loadMyList() {
  var myListContainer = document.getElementById('myListContainer');
  if (!myListContainer) return;
  
  var myList = JSON.parse(localStorage.getItem('myList') || '[]');
  var emptyState = document.getElementById('emptyState');
  
  if (myList.length === 0) {
    emptyState.style.display = 'block';
  } else {
    emptyState.style.display = 'none';
    myListContainer.innerHTML = '';
    
    myList.forEach(function(title) {
      var card = document.createElement('div');
      card.className = 'movie-card';
      card.onclick = function() { openModal(title); };
      
      card.innerHTML = '<img src="https://via.placeholder.com/250x350/51/e50914?text=' + encodeURIComponent(title) + '" alt="' + title + '">' +
                       '<div class="movie-info">' +
                       '<h3>' + title + '</h3>' +
                       '<p>In Your List</p>' +
                       '<div class="rating">★★★★☆</div>' +
                       '</div>';
      
      myListContainer.appendChild(card);
    });
  }
}

if (window.location.pathname.includes('mylist.html')) {
  loadMyList();
}

function slideMovies(section, direction) {
  var grid = document.getElementById(section + 'Grid');
  var scrollAmount = 300;
  grid.scrollBy({
    left: direction * scrollAmount,
    behavior: 'smooth'
  });
}

function filterGenre(genre) {
  var buttons = document.querySelectorAll('.filter-btn');
  buttons.forEach(function(btn) {
    btn.classList.remove('active');
  });
  
  var clickedButton = window.event.target;
  clickedButton.classList.add('active');
  
  var cards = document.querySelectorAll('.movie-card');
  cards.forEach(function(card) {
    if (genre === 'all' || card.getAttribute('data-genre') === genre) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

function handleSignIn(event) {
  event.preventDefault();
  var email = document.getElementById('signinEmail').value;
  var password = document.getElementById('signinPassword').value;
  
  if (email && password) {
    alert('Welcome back! Signing you in...');
    setTimeout(function() {
      window.location.href = 'browse.html';
    }, 1000);
  }
}

function handleSignUp(event) {
  event.preventDefault();
  var name = document.getElementById('signupName').value;
  var email = document.getElementById('signupEmail').value;
  var password = document.getElementById('signupPassword').value;
  var confirmPassword = document.getElementById('signupConfirmPassword').value;
  var plan = document.getElementById('signupPlan').value;
  
  if (password !== confirmPassword) {
    alert('Passwords do not match!');
    return;
  }
  
  if (name && email && password && plan) {
    alert('Account created successfully! Welcome to Netflix!');
    setTimeout(function() {
      window.location.href = 'browse.html';
    }, 1000);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  var cards = document.querySelectorAll('.movie-card');
  cards.forEach(function(card, index) {
    card.style.animationDelay = (index * 0.1) + 's';
  });
});