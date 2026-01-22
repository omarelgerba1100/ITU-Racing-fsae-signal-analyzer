"""
LaTeX equation rendering utility.
"""

import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

from ..core.config import COLORS


class LatexRenderer:
    """Render LaTeX equations to images."""

    @staticmethod
    def render_equation(equation: str, fontsize: int = 14, dpi: int = 150) -> Image.Image:
        """
        Render a LaTeX equation to a PIL Image.

        Args:
            equation: LaTeX equation string
            fontsize: Font size for rendering
            dpi: Resolution of output image

        Returns:
            PIL Image object containing the rendered equation
        """
        fig, ax = plt.subplots(figsize=(0.1, 0.1))
        ax.axis('off')

        text = ax.text(
            0.5, 0.5, f'${equation}$',
            fontsize=fontsize,
            ha='center', va='center',
            color='white',
            transform=ax.transAxes
        )

        fig.patch.set_facecolor(COLORS['bg_medium'])

        # Get the bounding box
        fig.canvas.draw()
        bbox = text.get_window_extent()

        # Resize figure to fit text
        width = bbox.width / dpi + 0.2
        height = bbox.height / dpi + 0.2
        fig.set_size_inches(width, height)

        # Save to buffer
        buf = io.BytesIO()
        fig.savefig(
            buf, format='png', dpi=dpi,
            facecolor=COLORS['bg_medium'],
            bbox_inches='tight', pad_inches=0.1
        )
        buf.seek(0)
        plt.close(fig)

        return Image.open(buf)

    @staticmethod
    def render_text(text: str, fontsize: int = 12, dpi: int = 150) -> Image.Image:
        """
        Render plain text to a PIL Image.

        Args:
            text: Text string to render
            fontsize: Font size for rendering
            dpi: Resolution of output image

        Returns:
            PIL Image object containing the rendered text
        """
        fig, ax = plt.subplots(figsize=(0.1, 0.1))
        ax.axis('off')

        text_obj = ax.text(
            0.5, 0.5, text,
            fontsize=fontsize,
            ha='center', va='center',
            color='white',
            family='monospace',
            transform=ax.transAxes
        )

        fig.patch.set_facecolor(COLORS['bg_medium'])

        fig.canvas.draw()
        bbox = text_obj.get_window_extent()

        width = bbox.width / dpi + 0.2
        height = bbox.height / dpi + 0.2
        fig.set_size_inches(width, height)

        buf = io.BytesIO()
        fig.savefig(
            buf, format='png', dpi=dpi,
            facecolor=COLORS['bg_medium'],
            bbox_inches='tight', pad_inches=0.1
        )
        buf.seek(0)
        plt.close(fig)

        return Image.open(buf)
