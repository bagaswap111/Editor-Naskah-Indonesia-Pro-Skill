document.addEventListener('DOMContentLoaded', function() {
    initializeScoreButtons();
    loadExistingData();
    startAutoSave();
});

function initializeScoreButtons() {
    var scoreButtons = document.querySelectorAll('.score-btn');
    
    scoreButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var dimension = this.dataset.dimension;
            var score = parseInt(this.dataset.score);
            
            var hiddenInput = document.querySelector('input[name="score_' + dimension + '"]');
            if (hiddenInput) {
                hiddenInput.value = score;
            }
            
            var group = this.closest('.score-buttons');
            group.querySelectorAll('.score-btn').forEach(function(btn) {
                btn.classList.remove('selected');
            });
            this.classList.add('selected');
            
            var commentGroup = document.getElementById('comment-' + dimension);
            if (commentGroup) {
                commentGroup.style.display = score <= 6 ? 'block' : 'none';
            }
        });
    });
}

function loadExistingData() {
    if (typeof existingScores !== 'undefined') {
        Object.keys(existingScores).forEach(function(dimension) {
            var score = existingScores[dimension];
            if (score !== null) {
                var button = document.querySelector(
                    '.score-btn[data-dimension="' + dimension + '"][data-score="' + score + '"]'
                );
                if (button) {
                    button.click();
                }
            }
        });
    }
    
    if (typeof existingComments !== 'undefined') {
        Object.keys(existingComments).forEach(function(dimension) {
            var comment = existingComments[dimension];
            if (comment) {
                var textarea = document.querySelector(
                    'textarea[name="comment_' + dimension + '"]'
                );
                if (textarea) {
                    textarea.value = comment;
                }
            }
        });
    }
}

function collectFormData() {
    var data = {
        manuscript_id: pageData.manuscriptId,
        output_type: pageData.outputType,
        page_number: pageData.pageNumber
    };
    
    var dimensions = ['kejelasan', 'koherensi', 'kedalaman', 'akurasi', 'gaya', 'mekanik', 'engagement'];
    dimensions.forEach(function(dim) {
        var input = document.querySelector('input[name="score_' + dim + '"]');
        data['score_' + dim] = input ? (input.value || null) : null;
        
        var textarea = document.querySelector('textarea[name="comment_' + dim + '"]');
        data['comment_' + dim] = textarea ? textarea.value : '';
    });
    
    return data;
}

function saveDraft() {
    var data = collectFormData();
    
    fetch('/api/evaluation/save-draft', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(function(response) { return response.json(); })
    .then(function(result) {
        if (result.success) {
            showNotification('Draft tersimpan', 'success');
        }
    })
    .catch(function(error) {
        console.error('Error saving draft:', error);
        showNotification('Gagal menyimpan draft', 'error');
    });
}

function submitAll() {
    var data = collectFormData();
    
    var dimensions = ['kejelasan', 'koherensi', 'kedalaman', 'akurasi', 'gaya', 'mekanik', 'engagement'];
    var missingScores = dimensions.filter(function(dim) { return !data['score_' + dim]; });
    
    if (missingScores.length > 0) {
        showNotification('Harap isi semua skor sebelum submit', 'error');
        return;
    }
    
    var missingComments = [];
    dimensions.forEach(function(dim) {
        var score = parseInt(data['score_' + dim]);
        if (score <= 6 && !data['comment_' + dim]) {
            missingComments.push(dim);
        }
    });
    
    if (missingComments.length > 0) {
        showNotification('Harap isi komentar untuk skor <= 6', 'error');
        return;
    }
    
    if (confirm('Yakin ingin submit evaluasi ini?')) {
        fetch('/api/evaluation/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(function(response) { return response.json(); })
        .then(function(result) {
            if (result.success) {
                showNotification('Evaluasi berhasil disubmit', 'success');
                setTimeout(function() {
                    if (pageData.pageNumber < pageData.totalPages) {
                        window.location.href = '/evaluate/' + (pageData.pageNumber + 1);
                    }
                }, 1000);
            }
        })
        .catch(function(error) {
            console.error('Error submitting:', error);
            showNotification('Gagal submit evaluasi', 'error');
        });
    }
}

function switchTab(type) {
    showNotification('Beralih ke ' + type.toUpperCase(), 'info');
}

var autoSaveInterval;
function startAutoSave() {
    autoSaveInterval = setInterval(function() {
        var data = collectFormData();
        var hasScores = Object.keys(data).some(function(key) {
            return key.indexOf('score_') === 0 && data[key];
        });
        if (hasScores) {
            saveDraft();
        }
    }, 30000);
}

function showNotification(message, type) {
    var notification = document.createElement('div');
    notification.className = 'notification ' + type;
    notification.textContent = message;
    notification.style.cssText = 'position:fixed;top:20px;right:20px;padding:15px 25px;background:' + 
        (type === 'success' ? '#D4AF37' : type === 'error' ? '#E94560' : '#1A1A2E') + 
        ';color:' + (type === 'success' ? '#1A1A2E' : '#FFFFFF') + 
        ';font-family:Inter,sans-serif;font-size:0.9rem;z-index:10000;animation:slideIn 0.3s ease;';
    
    document.body.appendChild(notification);
    
    setTimeout(function() {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(function() { notification.remove(); }, 300);
    }, 3000);
}

var style = document.createElement('style');
style.textContent = '@keyframes slideIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}@keyframes slideOut{from{transform:translateX(0);opacity:1}to{transform:translateX(100%);opacity:0}}';
document.head.appendChild(style);
