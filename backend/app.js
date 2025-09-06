let currentCredentialId = null;

async function issueCredential() {
    const fileInput = document.getElementById('passportFile');
    const issueBtn = document.getElementById('issueBtn');
    const loading = document.getElementById('loading1');
    const resultDiv = document.getElementById('issueResult');
    
    if (!fileInput.files[0]) {
        showResult('issueResult', 'Please select a passport file', 'error');
        return;
    }
    
    issueBtn.disabled = true;
    loading.style.display = 'block';
    resultDiv.innerHTML = '';
    
    try {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        const response = await fetch('/issue-credential', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentCredentialId = result.credential_id;
            showResult('issueResult', `✅ ${result.message}<br>Credential ID: ${result.credential_id.substring(0, 16)}...`, 'success');
            
            // Enable next step
            document.getElementById('verifyBtn').disabled = false;
            document.getElementById('step1').classList.add('completed');
            document.getElementById('step2').classList.add('active');
        } else {
            showResult('issueResult', `❌ Failed to issue credential`, 'error');
        }
    } catch (error) {
        showResult('issueResult', `❌ Error: ${error.message}`, 'error');
    } finally {
        issueBtn.disabled = false;
        loading.style.display = 'none';
    }
}

async function verifyAge() {
    const verifyBtn = document.getElementById('verifyBtn');
    const loading = document.getElementById('loading2');
    const resultDiv = document.getElementById('verifyResult');
    
    if (!currentCredentialId) {
        showResult('verifyResult', 'Please issue a credential first', 'error');
        return;
    }
    
    verifyBtn.disabled = true;
    loading.style.display = 'block';
    resultDiv.innerHTML = '';
    
    try {
        const response = await fetch('/verify-age', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                credential_id: currentCredentialId,
                min_age: 18
            })
        });
        
        const result = await response.json();
        
        if (result.success && result.proof_valid) {
            const status = result.is_old_enough ? '✅ VERIFIED' : '❌ FAILED';
            const message = result.is_old_enough ? 
                'You have successfully proven you are over 18!' : 
                'Age verification failed - you are under 18.';
            
            showResult('verifyResult', `${status} ${message}<br><br>🔐 Zero-knowledge proof generated and verified!`, 
                      result.is_old_enough ? 'success' : 'error');
            
            if (result.is_old_enough) {
                document.getElementById('step2').classList.add('completed');
                document.getElementById('step3').classList.add('active');
            }
        } else {
            showResult('verifyResult', `❌ Verification failed: Invalid proof`, 'error');
        }
    } catch (error) {
        showResult('verifyResult', `❌ Error: ${error.message}`, 'error');
    } finally {
        verifyBtn.disabled = false;
        loading.style.display = 'none';
    }
}

async function getStats() {
    try {
        const response = await fetch('/stats');
        const stats = await response.json();
        
        showResult('statsResult', 
            `📊 System Statistics:<br>
            Total Credentials Issued: ${stats.total_credentials}<br>
            Current Merkle Root: ${stats.merkle_root.substring(0, 16)}...<br>
            <br>All credentials are publicly auditable in the Merkle tree!`, 'info');
    } catch (error) {
        showResult('statsResult', `❌ Error fetching stats: ${error.message}`, 'error');
    }
}

function showResult(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.innerHTML = `<div class="result ${type}">${message}</div>`;
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('step1').classList.add('active');
    getStats(); // Load initial stats
});