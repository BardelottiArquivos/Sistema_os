function formatarCEP(input) {
    let cep = input.value.replace(/\D/g, '');
    if (cep.length > 5) {
        cep = cep.slice(0, 5) + '-' + cep.slice(5, 8);
    }
    input.value = cep;
}

function consultarCEP() {
    const cepInput = document.getElementById('id_cep');
    const cep = cepInput.value.replace(/\D/g, '');
    
    if (cep.length !== 8) {
        alert('CEP deve ter 8 dígitos');
        return;
    }
    
    const btn = document.getElementById('btnConsultarCEP');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Consultando...';
    btn.disabled = true;
    
    fetch(`/clientes/api/consultar-cep/?cep=${cep}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('id_logradouro').value = data.logradouro || '';
                document.getElementById('id_bairro').value = data.bairro || '';
                document.getElementById('id_cidade').value = data.cidade || '';
                document.getElementById('id_estado').value = data.estado || '';
                if (data.complemento) {
                    document.getElementById('id_complemento').value = data.complemento;
                }
                mostrarSucesso('CEP encontrado!');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao consultar CEP');
        })
        .finally(() => {
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
}

function mostrarSucesso(mensagem) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show mt-2';
    alertDiv.innerHTML = `
        ${mensagem}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.getElementById('cep-alert-container');
    if (container) {
        container.innerHTML = '';
        container.appendChild(alertDiv);
        setTimeout(() => alertDiv.remove(), 3000);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const cepInput = document.getElementById('id_cep');
    if (cepInput) {
        cepInput.addEventListener('input', function() {
            formatarCEP(this);
        });
    }
    
    const btn = document.getElementById('btnConsultarCEP');
    if (btn) {
        btn.addEventListener('click', consultarCEP);
    }
});
