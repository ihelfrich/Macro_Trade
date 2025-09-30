
import os

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def write_table(df, path):
    ensure_dir(path)
    if path.endswith('.tex'):
        df.to_latex(
            path,
            index=False,
            float_format=lambda x: f'{x:.4f}',
            escape=False,
        )
    else:
        df.to_csv(path, index=False)

def write_fig(fig, path):
    ensure_dir(path)
    fig.savefig(path)
