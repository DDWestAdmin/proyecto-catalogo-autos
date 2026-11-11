// Scripts globales interactivos para el proyecto
document.addEventListener("DOMContentLoaded", function () {
    // Auto-cierre de alertas tras 4 segundos
    const alertList = document.querySelectorAll('.alert');
    alertList.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000);
    });

    const passwordField = document.querySelector('#id_password1');
    const firstNameField = document.querySelector('#id_first_name');
    const lastNameField = document.querySelector('#id_last_name');

    if (passwordField && firstNameField && lastNameField) {
        const requirements = {
            length: function (password) {
                return password.length >= 8;
            },
            special: function (password) {
                return /[^a-zA-Z0-9]/.test(password);
            },
            number: function (password) {
                return /\d/.test(password);
            },
            uppercase: function (password) {
                return /[A-Z]/.test(password);
            },
            personal: function (password) {
                const normalizedPassword = password.trim().toLocaleLowerCase();
                const firstName = firstNameField.value.trim().toLocaleLowerCase();
                const lastName = lastNameField.value.trim().toLocaleLowerCase();
                return normalizedPassword !== '' &&
                    normalizedPassword !== firstName &&
                    normalizedPassword !== lastName;
            }
        };

        function updatePasswordRequirements() {
            Object.keys(requirements).forEach(function (requirementName) {
                const requirement = document.querySelector(
                    '[data-requirement="' + requirementName + '"] input'
                );
                const requirementMet = requirements[requirementName](passwordField.value);
                requirement.checked = requirementMet;
                const requirementRow = requirement.closest('.password-requirement');
                requirementRow.classList.toggle('is-valid', requirementMet);
                requirementRow.classList.toggle('is-invalid', !requirementMet);
            });
        }

        passwordField.addEventListener('input', updatePasswordRequirements);
        firstNameField.addEventListener('input', updatePasswordRequirements);
        lastNameField.addEventListener('input', updatePasswordRequirements);
        updatePasswordRequirements();
    }

    inicializarMenuAdmin();
});

// Alternar pestañas del menú
function inicializarMenuAdmin() {
    const adminMenu = document.querySelector('.admin-nav');
    if (!adminMenu) {
        return;
    }

    adminMenu.querySelectorAll('[data-section]').forEach(function (button) {
        button.addEventListener('click', function () {
            showSection(button.dataset.section, button);
        });
    });

    const activeButton = adminMenu.querySelector('[data-section].active') ||
        adminMenu.querySelector('[data-section]');
    if (activeButton) {
        showSection(activeButton.dataset.section, activeButton);
    }
}

function showSection(sectionName, button) {
    const section = document.getElementById('sec-' + sectionName);
    if (!section) {
        return;
    }

    document.querySelectorAll('.admin-section').forEach(function (item) {
        item.classList.toggle('active', item === section);
    });
    document.querySelectorAll('.admin-btn[data-section]').forEach(function (item) {
        item.classList.toggle('active', item === button);
    });
}

function abrirModalVehiculo() {
    const modalElement = document.getElementById('modalCrear');
    if (!modalElement || !window.bootstrap) {
        return;
    }

    bootstrap.Modal.getOrCreateInstance(modalElement).show();
}