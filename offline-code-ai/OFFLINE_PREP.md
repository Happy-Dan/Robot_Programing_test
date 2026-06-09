# Offline Preparation

## 1. インストールするもの

- Python 3.10+
- Ollama
- VS Code または普段使うエディタ

## 2. モデルを事前に保存

ネットがある状態で:

```powershell
ollama pull qwen2.5-coder:7b
```

PCが重い場合:

```powershell
ollama pull qwen2.5-coder:1.5b
```

## 3. オフライン動作確認

Wi-Fiを切ってから:

```powershell
ollama serve
```

別のPowerShellで:

```powershell
python .\offline_code_ai.py --ask "Pythonでリストを昇順にソートするコードを書いて"
```

回答が返れば準備完了です。

## 4. おすすめの使い方

授業資料から、自分が見てもよい範囲の内容だけを `notes` に入れてください。

```powershell
python .\offline_code_ai.py --context .\notes\python_cheatsheet.md
```

これでチートシートを参照しながら回答できます。
