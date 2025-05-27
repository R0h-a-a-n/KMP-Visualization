# KMP String Matching Visualizer

This project implements a step-by-step visualizer for the **Knuth-Morris-Pratt (KMP)** pattern matching algorithm using `matplotlib`. It highlights how the LPS (Longest Prefix Suffix) array is built and how the KMP algorithm progresses through the input text to find matches of the pattern.

![image](https://github.com/user-attachments/assets/ba362be9-e091-4be2-98c8-6b8482de06ff)


## Features

- Visual representation of:
  - LPS array construction
  - Matching phase with shifting and jumps
- Step-by-step animation controlled by keyboard input
- Boxed characters with color-coded states
- Dynamic updates of the current action and state

## Requirements

- Python 3.7+
- `matplotlib` (for animation and drawing)

To install the dependencies:

```bash
pip install matplotlib
```

Or if you're using Anaconda:

```bash
conda install matplotlib
```

## How to Run
```bash
python final.py
```

