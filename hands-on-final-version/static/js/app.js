// 資産管理アプリのフロントエンドJavaScript

// APIのベースURL
const API_BASE_URL = '/api';

// アプリケーションの状態管理
let assets = [];

// DOM要素の取得
const assetForm = document.getElementById('asset-form');
const assetsTable = document.getElementById('assets-table');
const assetsTbody = document.getElementById('assets-tbody');

// ユーティリティ関数
function formatCurrency(amount) {
    return new Intl.NumberFormat('ja-JP', {
        style: 'currency',
        currency: 'JPY'
    }).format(amount);
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


// UI更新関数
function renderAssets() {
    const tbody = document.getElementById('assets-tbody');
    tbody.innerHTML = '';

    if (assets.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="2" class="px-4 py-8 text-center text-gray-500">
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
        `;
        tbody.appendChild(row);
    });
}

// イベントハンドラー
async function handleAssetSubmit(event) {
    event.preventDefault();

    const formData = new FormData(assetForm);
    const assetData = {
        name: formData.get('name'),
        amount: parseFloat(formData.get('amount'))
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



// イベントリスナーの設定
function setupEventListeners() {
    assetForm.addEventListener('submit', handleAssetSubmit);
}

// アプリケーションの初期化
async function initApp() {
    setupEventListeners();
    await fetchAssets();
}

// ページ読み込み時の初期化
document.addEventListener('DOMContentLoaded', initApp); 