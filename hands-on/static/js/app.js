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
// fetch()を使用してGET /api/assetsを呼び出し、レスポンスをJSONで取得してください
async function fetchAssets() {
    // TODO: 資産一覧を取得するAPI通信関数を実装してください
}

// fetch()を使用してPOST /api/assetsを呼び出し、JSONデータを送信してください
async function createAsset(assetData) {
    // TODO: 資産を作成するAPI通信関数を実装してください
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
// FormDataを使用してフォームデータを取得し、createAsset()を呼び出してください
async function handleAssetSubmit(event) {
    // TODO: フォーム送信時のイベントハンドラーを実装してください
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

// アプリケーションの開始
document.addEventListener('DOMContentLoaded', initApp); 