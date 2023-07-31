# LEGEND Plot Blessing Plots

Repo with all official plots ...

In parallel to uploading the plot here, please also prepare a description of the plot on the dedicated Confluence page ...


## LEGEND plot style:

This repository also provides a small extension to the matplotlib library in order to have some consistent plotting style for LEGEND. You can install the extension using the following instructions:

1. Download the githup repository using:
```
git clone git@github.com:valerioda/legendPlots.git
```

2. Install the package via:
```
pip install -e legendPlots/
```

3. Import the LEGEND plotting style via: 
```
from legend_plot_style import LEGENDPlotStyle
# all other imports
```
WARNING: Please make sure that you import the `LEGENDPlotStyle` package first. If another package initalizes matplotlib first the extension wont work.

After importing the extension you have access to the LEGEND plotting style and the LEGEND logo as watermark. You can add the water mark to a corresponding axes in the following way:
```
fix, axes = plt.subplots()
axes.set_legend_logo('upper right')
```
By default the LEGEND dark logo is used. You can change the logo type, size and transparency via the provided keyword arguments. The size of the logo is automatically resized based on the figure size and the specified scaling_factor. Please do not hesistate to consult the python-help by pressing "shift" + "tab" or by calling `help(axes.set_legend_logo)` in your notebook for more information. 