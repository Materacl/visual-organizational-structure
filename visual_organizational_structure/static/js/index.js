const showDeleteFormBtn = document.querySelectorAll('[id=show-delete-form-btn]');
const DeleteDashboardForm = document.querySelectorAll('[id=delete-dashboard-form]');
const CancelDeleteDash = document.getElementById('CancelDeleteDash');
showDeleteFormBtn.forEach((btn, index) => {
    btn.addEventListener('click', () => {
        DeleteDashboardForm[index].style.display = 'block';
    });
});

// JavaScript to toggle the create dashboard form and text
document.addEventListener('DOMContentLoaded', function () {

    const showCreateFormBtn = document.getElementById('show-create-form-btn');
    const createDashboardForm = document.getElementById('create-dashboard-form');
    const createDashboardText = document.getElementById('create-dashboard-text');


    showCreateFormBtn.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the default action of the anchor tag
        if (createDashboardForm.style.display === 'none' || !createDashboardForm.style.display) {
            createDashboardForm.style.display = 'block';
            createDashboardForm.style.opacity = '1'; // Ensure form is visible
        } else {
            createDashboardForm.style.display = 'none';
            createDashboardForm.style.opacity = '0'; // Hide form
            createDashboardText.textContent = 'Создать доску';
        }
    });

    // Close the form when clicked outside of it
    document.addEventListener('click', function (event) {
        if (!createDashboardForm.contains(event.target) && !showCreateFormBtn.contains(event.target)) {
            createDashboardForm.style.display = 'none';
            createDashboardForm.style.opacity = '0';
            createDashboardText.textContent = 'Создать доску';
        }
    });



});