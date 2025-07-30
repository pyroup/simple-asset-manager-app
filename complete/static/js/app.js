// 資産管理アプリのフロントエンドJavaScript（完成版）

// APIのベースURL
const API_BASE_URL = '/api';

// アプリケーションの状態管理
let assets = [];

// DOM要素の取得
const assetForm = document.getElementById('asset-form');
const assetsTable = document.getElementById('assets-table');
const assetsTbody = document.getElementById('assets-tbody');
const refreshButton = document.getElementById('refresh-assets');
const editModal = document.getElementById('edit-modal');
const editForm = document.getElementById('edit-form');
const cancelEditButton = document.getElementById('cancel-edit');

// ユーティリティ関数
function formatCurrency(amount) {
    return new Intl.NumberFormat('ja-JP', {
        style: 'currency',
        currency: 'JPY'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('ja-JP');
}

function getCategoryBadgeClass(category) {
    const categoryMap = {
        '現金': 'cash',
        '預金': 'deposit',
        '株式': 'stock',
        '不動産': 'real-estate',
        '投資信託': 'fund',
        'その他': 'other'
    };
    return categoryMap[category] || 'other';
}

function showMessage(message, type = 'success') {
    // 既存のメッセージを削除
    const existingMessage = document.querySelector('.message');
    if (existingMessage) {
        existingMessage.remove();
    }

    // 新しいメッセージを作成
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;

    // ページ上部に挿入
    const header = document.querySelector('header');
    header.parentNode.insertBefore(messageDiv, header.nextSibling);

    // 3秒後に自動で削除
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 3000);
}

function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="loading"></div>';
    }
}

function hideLoading(element) {
    if (element) {
        element.innerHTML = '';
    }
}

// API通信関数
async function fetchAssets() {
    try {
        const response = await fetch(`${API_BASE_URL}/assets`);
        if (!response.ok) {
            throw new Error('資産の取得に失敗しました');
        }
        assets = await response.json();
        renderAssets();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function createAsset(assetData) {
    try {
        const response = await fetch(`${API_BASE_URL}/assets`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(assetData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '資産の作成に失敗しました');
        }

        return await response.json();
    } catch (error) {
        throw error;
    }
}

async function updateAsset(assetId, assetData) {
    try {
        const response = await fetch(`${API_BASE_URL}/assets/${assetId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(assetData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '資産の更新に失敗しました');
        }

        return await response.json();
    } catch (error) {
        throw error;
    }
}

async function deleteAsset(assetId) {
    try {
        const response = await fetch(`${API_BASE_URL}/assets/${assetId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '資産の削除に失敗しました');
        }

        return await response.json();
    } catch (error) {
        throw error;
    }
}



// UI更新関数
function renderAssets() {
    const tbody = document.getElementById('assets-tbody');
    tbody.innerHTML = '';

    if (assets.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="px-4 py-8 text-center text-gray-500">
                    資産が登録されていません
                </td>
            </tr>
        `;
        return;
    }

    assets.forEach(asset => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-4 py-2">${asset.name}</td>
            <td class="px-4 py-2 amount">${formatCurrency(asset.amount)}</td>
            <td class="px-4 py-2">${asset.quantity}</td>
            <td class="px-4 py-2">
                <span class="category-badge ${getCategoryBadgeClass(asset.category)}">
                    ${asset.category}
                </span>
            </td>
            <td class="px-4 py-2">
                <button onclick="handleEditAsset(${JSON.stringify(asset).replace(/"/g, '&quot;')})" 
                        class="bg-blue-500 text-white px-2 py-1 rounded text-sm mr-2 hover:bg-blue-600">
                    編集
                </button>
                <button onclick="handleDeleteAsset(${asset.id})" 
                        class="bg-red-500 text-white px-2 py-1 rounded text-sm hover:bg-red-600">
                    削除
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}



function populateEditForm(asset) {
    document.getElementById('edit-id').value = asset.id;
    document.getElementById('edit-name').value = asset.name;
    document.getElementById('edit-amount').value = asset.amount;
    document.getElementById('edit-quantity').value = asset.quantity;
    document.getElementById('edit-category').value = asset.category;
    document.getElementById('edit-description').value = asset.description || '';
}

function clearEditForm() {
    document.getElementById('edit-id').value = '';
    document.getElementById('edit-name').value = '';
    document.getElementById('edit-amount').value = '';
    document.getElementById('edit-quantity').value = '1';
    document.getElementById('edit-category').value = '現金';
    document.getElementById('edit-description').value = '';
}

// イベントハンドラー
async function handleAssetSubmit(event) {
    event.preventDefault();

    const formData = new FormData(assetForm);
    const assetData = {
        name: formData.get('name'),
        amount: parseFloat(formData.get('amount')),
        quantity: parseInt(formData.get('quantity')),
        category: formData.get('category'),
        description: formData.get('description')
    };

    try {
        await createAsset(assetData);
        showMessage('資産を登録しました');
        assetForm.reset();
        await fetchAssets();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function handleEditSubmit(event) {
    event.preventDefault();

    const assetId = document.getElementById('edit-id').value;
    const assetData = {
        name: document.getElementById('edit-name').value,
        amount: parseFloat(document.getElementById('edit-amount').value),
        quantity: parseInt(document.getElementById('edit-quantity').value),
        category: document.getElementById('edit-category').value,
        description: document.getElementById('edit-description').value
    };

    try {
        await updateAsset(assetId, assetData);
        showMessage('資産を更新しました');
        handleCancelEdit();
        await fetchAssets();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function handleDeleteAsset(assetId) {
    if (!confirm('この資産を削除しますか？')) {
        return;
    }

    try {
        await deleteAsset(assetId);
        showMessage('資産を削除しました');
        await fetchAssets();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

function handleEditAsset(asset) {
    populateEditForm(asset);
    editModal.classList.add('show');
}

function handleCancelEdit() {
    clearEditForm();
    editModal.classList.remove('show');
}

async function handleRefresh() {
    try {
        await fetchAssets();
        showMessage('データを更新しました');
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// イベントリスナーの設定
function setupEventListeners() {
    assetForm.addEventListener('submit', handleAssetSubmit);
    editForm.addEventListener('submit', handleEditSubmit);
    cancelEditButton.addEventListener('click', handleCancelEdit);
    refreshButton.addEventListener('click', handleRefresh);

    // モーダルの外側をクリックした時に閉じる
    editModal.addEventListener('click', (event) => {
        if (event.target === editModal) {
            handleCancelEdit();
        }
    });
}

// アプリケーションの初期化
async function initApp() {
    setupEventListeners();
    await fetchAssets();
}

// ページ読み込み時の初期化
document.addEventListener('DOMContentLoaded', initApp); 