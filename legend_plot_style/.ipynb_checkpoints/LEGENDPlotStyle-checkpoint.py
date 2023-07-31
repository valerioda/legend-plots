import matplotlib
import matplotlib.axes
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox, AnnotationBbox
from PIL import Image
import sys
import os
import warnings
import numpy as np
from pathlib import PurePath


class LEGENDAxes(matplotlib.axes.Axes):
    """
    Class to overwrite matplotlib.axes.Axes class with a custom made
    class for LEGEND. It is basically the same as the default matplotlib 
    class, but with some additional features.
    
    The basics ideas are taken from
    https://stackoverflow.com/questions/56981603/matplotlib-add-a-default-watermark
    and
    https://stackoverflow.com/questions/43842567/matplotlib-automate-placement-of-watermark
    """
    def __init__(self, *args, **kwargs):
        path = __file__
        path = path.split('/')[:-1]
        self.logo_dir = os.path.join('/'.join(path), 'logos')
        self.logo_dict = {'dark_preliminary': 'logo_legend_dkbl_preliminary.png',
                          'dark': 'logo_legend_dkbl.png'
                         }
        super().__init__(*args, **kwargs)
    
    def set_legend_logo(self, position, logo_type='dark',
                       alpha=0.8, scaling_factor=6, dpi=600):
        """
        Adds to selected axes the LEGEND logo as a water mark.
        
        Args:
            position (str):  Can be any of 'upper right', 'upper left', 
                'lower left', 'lower right', 'center left', 'center right',
                'lower center', 'upper center', 'center'
            logo_type (str): Can be either ('dark', 'dark_preliminary').
            alpha (float): Transparency of the logo.
            scaling_factor (float): The logo will be scaled by figsize x 1/scaling_factor.
            dpi (int): dots per inch of the plot.
        """        
        logo_file_name = self.logo_dict[logo_type]     
        logo_path = os.path.join(self.logo_dir, logo_file_name)
        water_mark = self.watermark(position, alpha, logo_path,
                                    scaling_factor, dpi)
        return water_mark    
    
    def watermark(self, position, alpha, logo_path, scaling_factor, dpi):
        
        imagebox = self.get_imagebox(alpha=alpha, 
                                     logo_path=logo_path, 
                                     scaling_factor=scaling_factor, 
                                     dpi=dpi)
        if isinstance(position, str):
            water_mark = AnchoredOffsetbox(loc=position, 
                                           pad=0.5, 
                                           borderpad=0, 
                                           child=imagebox,
                                          )
        else:
            water_mark = AnnotationBbox(imagebox, 
                                        xy=position,
                                        pad=0.5, 
                                        frameon = False)

        water_mark.patch.set_alpha(0)
        self.add_artist(water_mark)   
        return water_mark
    
    def get_imagebox(self, alpha, logo_path, scaling_factor, dpi):
        img = Image.open(logo_path)
        img = self._resize_image(self.figure, img, scaling_factor, dpi)
        imagebox = OffsetImage(img,
                               zoom=72/dpi, # 72 is the standard dpi in matplotlib
                               alpha=alpha)
        return imagebox
    
    @staticmethod
    def _resize_image(fig, image, scaling_factor=10, dpi=600):
        """
        Sizes an image based on the figure size and the specified scaling_factor.
        
        The image is scaled such that its width corresponds to 1/scaling_factor of
        the figure width.
        """
        width, height = fig.get_size_inches()*dpi
        wm_width = int(width/scaling_factor) 
        scaling = (wm_width / float(image.size[0]))
        wm_height = int(float(image.size[1])*float(scaling))
        image = image.resize((wm_width, wm_height), Image.ANTIALIAS)
        return image
matplotlib.axes.Axes = LEGENDAxes
"""
class LEGENDLegend(matplotlib.legend.Legend):
    
    #Class to overwrite matplotlib.legend.Legend class with a custom made
    #class for LEGEND. This only changes some of the default values.

    def __str__(self):
        return "Legend"

    def __init__(
        self, parent, handles, labels,
        ncol=2,     # number of columns
        bbox_to_anchor=(0.5,1),  # bbox to which the legend will be anchored
        **kwargs
    ):
        super().__init__(parent,
                         handles,
                         labels,
                         ncol=ncol,
                         bbox_to_anchor=bbox_to_anchor,
                         **kwargs)

file_name = os.path.basename(__file__).split('.')[0]
if 'matplotlib.pyplot' in sys.modules.keys():
    warnings.warn('It looks like "matplotlib.pyplot" has been already initialized. '
                  'You are risking going down a dark road with no return. '
                  'Many hours were spent by the elder magician to make this dark '
                  'art work, but they failed. If you do not want to wander in '
                  f'their footsteps of doom, make sure you import "{file_name}" ' 
                  'first before any other module.')

matplotlib.legend.Legend = LEGENDLegend"""

def use(style):
    """Wrapper around matplotlib.pyplot.style.use, which takes care of the location
    of stylesheets.

    Args:
        style (str or list of str): name(s) of matplotlib stylesheet(s) inside styles folder.
    """
    from matplotlib import pyplot
    path = __file__
    path = os.path.split(path)[0]

    if isinstance(style, str):
        styles = [style]
    else:
        styles = style
    for i,s in enumerate(styles):
        sname = os.path.join(path, 'styles', s + '.mplstyle')
        if os.path.isfile(sname):
            styles[i] = sname
    
    pyplot.style.use(styles)


def figure(rescale=None, **kwargs):
    """Wrapper around matplotlib.pyplot.figure fith an additional rescale option.

    Args:
        rescale (tuple of floats, optional): Rescales the default figsize by the values in the tuple (w, h).
                                             Defaults to None.

    Returns:
        figure: matplotlib figure
    """
    import matplotlib.pyplot as plt
    
    figsize_kw = kwargs.pop('figsize', None)
    figsize_rc = plt.rcParams['figure.figsize']
    
    (fig_width, fig_height) = _get_figsize(figsize_kw, figsize_rc, rescale)
    fig = plt.figure(figsize=(fig_width, fig_height), **kwargs)
    return fig

def subplots(nrows=1,
             ncols=1,
             rescale=None,
             **kwargs):
    """Wrapper around matplotlib.pyplot.subplots fith an additional rescale option.

    Args:
        nrows / ncols (int): Number of rows/columns of the subplot grid. Default to 1.
        rescale (tuple of floats, optional): Rescales the default figsize by the values in the tuple (w, h).
                                             Defaults to None.

    Returns:
        figure, axes: matplotlib figure and axes
    """
    import matplotlib.pyplot as plt
    
    figsize_kw = kwargs.pop('figsize', None)
    figsize_rc = plt.rcParams['figure.figsize']
    
    (fig_width, fig_height) = _get_figsize(figsize_kw, figsize_rc, rescale)
    
       
    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(fig_width, fig_height),
                             **kwargs)
    return fig, axes
    
def _get_figsize(figsize_kw, figsize_rc, rescale):
    if figsize_kw is not None and rescale is not None:
        raise ValueError(f'Passing a value for figsize and rescale is ambiguous.')
    
    elif figsize_kw is None and rescale is None:
        (fig_width, fig_height) = figsize_rc
    
    elif figsize_kw is not None:
        (fig_width, fig_height) = figsize_kw
       
    elif rescale is not None:
        (fig_width, fig_height) = (figsize_rc[0] * rescale[0],
                                   figsize_rc[1] * rescale[1])
            
    return (fig_width, fig_height)

def get_colors():
    return {
    'black': '#000000',
    'legend_grey': "#CCCCCC",
    'legend_blue': "#07A9FF",
    'legend_darkblue': "#1A2A5B",
    'red': "#B9123E",
    'yellow': "#ffc74e",
    'green': "#39a974",
    'purple': '#8A1859',
    'silver': '#BFC2C7',
    'salmon': '#FFB0A8',
    'violet': '#B580CA',
    'darkblue': "#203769",
    'grey': "#909090",
    'gray': "#909090",
    '1sigma_green': '#83C369',
    '2sigma_yellow': '#FDED95',
    'mint': '#85F7C2',
    'forestgreen': '#105D20',
    'orange': '#E77D4D',
    'darkred': '#9D0008',
    'sand': '#EDDAB7',
    'lightgrey': '#DCDCDC',
    'lightgray': '#DCDCDC',
    'jet': '#393939',
    'teal': '#149A9A',
          }

colors = get_colors()

def darkmode_colors():
    """
        Function to invert the colors of some darkmode-incompatible colors
    """
    colors["black"] = "#FFFFFF"


def plot_colortable(c=None, title='XENONnT Colors', sort_colors=True, emptycols=0):
    """
    Plot overview of XENONnT colors.
    From https://matplotlib.org/3.5.0/gallery/color/named_colors.html
    """
    from matplotlib.patches import Rectangle
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    
    if c is None:
        c = colors
        
    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12
    topmargin = 40

    # Sort colors by hue, saturation, value and name.
    if sort_colors is True:
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                         name)
                        for name, color in c.items())
        names = [name for hsv, name in by_hsv]
    else:
        names = list(c)

    n = len(names)
    ncols = 4 - emptycols
    nrows = n // ncols + int(n % ncols > 0)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + margin + topmargin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=200)
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()
    ax.set_title(title, fontsize=24, loc="left", pad=10)

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(
            Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                      height=18, facecolor=c[name], edgecolor='0.7')
        )

    return fig

def get_optimal_figsize(width_pt, scale=1, ratio=2/3):
    # Shamelessly stolen from http://bkanuka.com/posts/native-latex-plots/
    """Little helper function to get the figsize for a given linewidth in pt
    of a LaTeX document in inches.

    Args:
        width_pt (float): \the\linewidth or \the\textwidth in pt.
        scale (float): fraction of the figure width from the full linewidth.
                        Defaults to 1
        

    Returns:
        tuple: figure size
    """
    inches_per_pt = 1.0 / 72.27                     # Convert pt to inch
    fig_width = width_pt * inches_per_pt * scale    # width in inches
    fig_height = fig_width * ratio                  # height in inches
    fig_size = (fig_width, fig_height)
    return fig_size
