/*---------menu icon navbar----------------*/

let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
};



/*----------scroll sections active links ----------------*/

let sections = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header nav a');

window.onscroll = () => {
    sections.forEach(sec => {
        let top = window.scrollY;
        let offset = sec.offsetTop - 150;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');

        if(top >= offset && top < offset + height) {
            navLinks.forEach(links => {
                links.classList.remove('active');
                document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
            });
        };
    });

/* -----------sticky navbar--------------*/
let header = document.querySelector('.header');
header.classList.toggle('sticky',window.scrollY > 100);

/*----------remove menu icon navbar when click navbar link---------------*/

menuIcon.classList.remove('bx-x');
navbar.classList.remove('active');

};

/*----------Dark light mode---------------*/
let darkModeIcon = document.querySelector('#darkMode-icon');

darkModeIcon.onclick = () => {
    darkModeIcon.classList.toggle('bx-sun');
    document.body.classList.toggle('dark-mode');
}

/*----------scroll reveal---------------
ScrollReveal({
    reset: true,
    distance: '80px',
    duration: 2000,
    delay: 200
});

ScrollReveal.reveal('.home-content, .heading', { origin: 'top' });
ScrollReveal.reveal('.home-img img, .services-container, .portfolio-box, .contact form', { origin: 'bottom' });
ScrollReveal.reveal('.home-content h1, .about-img img', { origin: 'left' });
ScrollReveal.reveal('.home-content h3, .home-content p, .about-content', { origin: 'right' });*/

function toggleChatbox() {
    var chatbox = document.querySelector('.chat-container');
    
    if (chatbox.style.display === 'none' || chatbox.style.display === '') {
        chatbox.classList.add('open');
        chatbox.classList.remove('close');
    } else {
        chatbox.classList.add('close');
        chatbox.classList.remove('open');
    }
    setTimeout(function() {
        chatbox.style.display = (chatbox.style.display === 'none' || chatbox.style.display === '') ? 'block' : 'none';
    }, 300);
}

function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    var chatDisplay = document.getElementById('chat-display');
    chatDisplay.innerHTML += '<div class="message user">' + userInput + '</div>';
    document.getElementById('user-input').value = '';

    // Send user input to the server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_input: userInput,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Introduce a slight delay before displaying the bot's response
        setTimeout(function() {
            var botResponse = data.bot_response;
            chatDisplay.innerHTML += '<div class="message bot">' + botResponse + '</div>';
            chatDisplay.scrollTop = chatDisplay.scrollHeight; // Auto-scroll to the latest message
        }, 500); // Adjust the delay duration as needed
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
}

// Event listener for Enter key
document.getElementById('user-input').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

// Event listener for Esc key
document.addEventListener('keyup', function(event) {
    if (event.key === 'Escape') {
        // Hide the chat dialogue box (you may need to implement your logic here)
        var chatbox = document.querySelector('.chat-container');
        chatbox.style.display = 'none';
    }
});

/*----Experienced years-----*/

var startDate = new Date('2015-09-16');
var currentDate = new Date();
var yearsExperience = currentDate.getFullYear() - startDate.getFullYear();
document.getElementById('experience-years').textContent = yearsExperience;

/*---Download CV -----*/

function downloadCV(event) {
    event.preventDefault();

    var link = document.getElementById('download-link');
    if (link) {
        document.body.removeChild(link);
    }
    link = document.createElement('a');
    link.href = '/static/Resume/Harihara_Ganesh.pdf';
    link.download = 'Harihara_Ganesh.pdf';
    link.id = 'download-link';

    document.body.appendChild(link);
    link.click();
}

/*--Read me ----*/

function toggleContent() {
    event.preventDefault();
    var content = document.getElementById('expand-content');
    content.classList.toggle('hidden');
    content.classList.toggle('expanded');
}

/*----Send Message----*/

function initializeContactForm() {
    document.addEventListener('DOMContentLoaded', function () {
        const contactForm = document.querySelector('#contact-form');

        contactForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            try {
                const formData = new FormData(contactForm);
                await fetch('/send_message', {
                    method: 'POST',
                    body: formData,
                });
                Swal.fire({
                    icon: 'success',
                    title: 'Message sent successfully!',
                    showConfirmButton: false,
                    timer: 1500
                }).then(() => {
                    contactForm.reset();
                });
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
}

initializeContactForm();

/*---Service Modal----*/

function openModal(serviceName, event) {
    event.preventDefault();

    var modal = document.getElementById("myModal");
    var modalTitle = document.getElementById("modal-title");
    var modalContent = document.getElementById("modal-content");

    switch (serviceName) {
        case 'Web Development':
            modalTitle.innerHTML = "Web Development Services";
            modalContent.innerHTML = "1. How we can build your web.<br>2. What tech stacks we can use.<br>3. How the process begins from start till deployment.<br>4. How we can modify based on your requirements.";
            break;
        default:
            break;
    }

    modal.style.display = "block";

    window.addEventListener("keydown", function (event) {
        if (event.key === "Escape" || event.key === "Esc") {
            closeModal();
        }
    });
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
    window.removeEventListener("keydown", function () {});
}

window.onclick = function (event) {
    var modal = document.getElementById("myModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}