function showHelp() {
    document.getElementById('helpModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeHelp() {
    document.getElementById('helpModal').classList.remove('active');
    document.body.style.overflow = '';
}

window.onclick = function(event) {
    const modal = document.getElementById('helpModal');
    if (event.target === modal) {
        closeHelp();
    }
}

function toggleOtherService() {
    const type = document.getElementById('serviceType').value;
    const customGroup = document.getElementById('customServiceGroup');
    const standardGroup = document.getElementById('standardServiceGroup');
    const customInput = document.getElementById('customServiceInput');
    const standardInput = document.getElementById('standardServiceTitle');
    
    if (type === 'Otros') {
        customGroup.style.display = 'block';
        standardGroup.style.display = 'none';
        customInput.setAttribute('required', 'true');
        customInput.name = "service_title_custom";
        standardInput.removeAttribute('name');
        standardInput.removeAttribute('required');
    } else {
        customGroup.style.display = 'none';
        standardGroup.style.display = 'block';
        customInput.removeAttribute('required');
        customInput.removeAttribute('name');
        standardInput.name = "service_title_std";
        standardInput.setAttribute('required', 'true');
    }
}

function toggleMaterials() {
    const checkbox = document.getElementById('hasMaterials');
    const options = document.getElementById('materialsOptions');
    options.style.display = checkbox.checked ? 'block' : 'none';
}

function calcRemaining() {
    const structure = document.getElementById('payStructure').value;
    const total = parseFloat(document.getElementById('totalAmount').value) || 0;
    const advanceInput = document.getElementById('advanceAmount');
    const remainingInput = document.getElementById('remainingAmount');
    const advanceDiv = document.getElementById('advanceDiv');
    const remainingDiv = document.getElementById('remainingDiv');
    
    if (structure === 'advance' || structure === 'partial') {
        advanceDiv.style.display = 'block';
        remainingDiv.style.display = 'block';
        const advance = parseFloat(advanceInput.value) || 0;
        remainingInput.value = (total - advance).toFixed(2);
    } else {
        advanceDiv.style.display = 'none';
        remainingDiv.style.display = 'none';
        advanceInput.value = '';
        remainingInput.value = '';
    }
}

function togglePaymentDetails() {
    const method = document.getElementById('payMethod').value;
    document.getElementById('bankDetails').style.display = 'none';
    document.getElementById('cryptoDetails').style.display = 'none';
    document.getElementById('otherDetails').style.display = 'none';
    
    if (method === 'transfer') {
        document.getElementById('bankDetails').style.display = 'block';
    } else if (method === 'crypto') {
        document.getElementById('cryptoDetails').style.display = 'block';
    } else if (method === 'other') {
        document.getElementById('otherDetails').style.display = 'block';
    }
}

function togglePenalties() {
    const timing = document.getElementById('payTiming').value;
    const penaltySection = document.getElementById('penaltyInput');
    const checkbox = document.getElementById('applyPenalty');
    
    if (timing === 'before') {
        penaltySection.style.display = 'none';
        checkbox.checked = false;
    } else {
        if (checkbox.checked) {
            penaltySection.style.display = 'block';
        }
    }
}

function togglePenaltyInput() {
    const checkbox = document.getElementById('applyPenalty');
    const input = document.getElementById('penaltyInput');
    input.style.display = checkbox.checked ? 'block' : 'none';
}

function toggleAdvanced() {
    const panel = document.getElementById('advancedOptions');
    panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
}

function toggleSignatureNames() {
    const checkbox = document.getElementById('includeSignatures');
    const namesDiv = document.getElementById('signatureNames');
    namesDiv.style.display = checkbox.checked ? 'grid' : 'none';
}

function previewLogo(input) {
    const preview = document.getElementById('logoPreview');
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.remove('hidden');
        }
        reader.readAsDataURL(input.files[0]);
    } else {
        preview.classList.add('hidden');
    }
}

document.getElementById('contractForm').addEventListener('submit', function(e) {
    const total = parseFloat(document.getElementById('totalAmount').value);
    if (isNaN(total) || total <= 0) {
        e.preventDefault();
        alert("El monto total debe ser mayor a 0.");
        return false;
    }
    
    const customInput = document.getElementById('customServiceInput');
    if (document.getElementById('customServiceGroup').style.display === 'block' && !customInput.value.trim()) {
        e.preventDefault();
        alert("Especifica el tipo de servicio personalizado.");
        return false;
    }
    
    const checkbox = document.getElementById('applyPenalty');
    const penaltyInput = document.querySelector('#penaltyInput input');
    if (checkbox.checked && (!penaltyInput.value || parseFloat(penaltyInput.value) <= 0)) {
        e.preventDefault();
        alert("Ingrese un valor de penalización válido (> 0).");
        return false;
    }
});

setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        alert.style.transition = 'opacity 0.5s';
        alert.style.opacity = '0';
        setTimeout(function() {
            alert.remove();
        }, 500);
    });
}, 5000);
