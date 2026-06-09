# Offline Code AI

大学のプログラミングテスト中にネットワークなしで使うための、ローカルLLM用コード生成AIです。

このプロジェクト自体はネットを使いません。AIモデルの実行には、事前にローカル推論ソフトとモデルをPCへ入れておく必要があります。

## 仕組み

- `offline_code_ai.py` がローカルの Ollama API に質問を送ります。
- モデルはPC上で動くので、試験中にネットが切れても動作します。
- Python標準ライブラリだけで作っているため、`pip install` は不要です。
- 自分のノートや授業資料の抜粋を `--context` で渡せます。

## 必要な環境

テスト前に、ネットがある状態で次を準備してください。

1. Python 3.10 以上
2. Ollama
3. コード向けモデル

推奨モデル例:

- 軽め: `qwen2.5-coder:1.5b`
- バランス: `qwen2.5-coder:7b`
- PC性能に余裕がある場合: `qwen2.5-coder:14b`

Windowsなら、まず Python と Ollama をインストールしてから PowerShell で次を実行します。

```powershell
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b
```

一度モデルをダウンロードしておけば、以後はオフラインで使えます。

## 起動

Ollamaを起動します。

```powershell
ollama serve
```

別のPowerShellで、このフォルダに移動して実行します。

```powershell
.\run.ps1
```

または直接:

```powershell
python .\offline_code_ai.py
```

## 環境チェック

PythonやOllamaが入っているか確認するには:

```powershell
.\check_env.ps1
```

もしPowerShellの実行ポリシーで止まる場合:

```powershell
powershell -ExecutionPolicy Bypass -File .\check_env.ps1
```

## 使い方

対話モード:

```powershell
python .\offline_code_ai.py
```

1回だけ質問:

```powershell
python .\offline_code_ai.py --ask "Pythonで標準入力を1行ずつ読む方法を教えて"
```

ファイルを見せて質問:

```powershell
python .\offline_code_ai.py --context .\notes\python_cheatsheet.md --ask "辞書の使い方を短く復習したい"
```

ソースコードを説明:

```powershell
python .\offline_code_ai.py --explain .\templates\python_basic.py
```

モデル名を変える:

```powershell
python .\offline_code_ai.py --model qwen2.5-coder:1.5b
```

## 試験前チェックリスト

- [ ] Python が `python --version` で動く
- [ ] Ollama が `ollama --version` で動く
- [ ] モデルを `ollama pull ...` でダウンロード済み
- [ ] `ollama run qwen2.5-coder:7b` がネットなしで起動する
- [ ] Wi-Fiを切った状態で `python .\offline_code_ai.py --ask "hello"` が動く
- [ ] 授業資料、ノート、テンプレートをローカル保存した
- [ ] テストでAI利用が許可されているか確認した

## 注意

試験では、生成AIやローカル資料の利用が禁止されている場合があります。授業や試験のルールを必ず確認してください。

また、AIの回答は間違うことがあります。テスト中は「コードの候補を出す道具」として使い、最終的な判断は自分で確認してください。
