import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import save_fig as sf

# s = pd.Series(np.arange(5), index=list('abcde'))
# ax = s.plot()
# # print(type(ax))
# # <class 'matplotlib.axes._subplots.AxesSubplot'>
# # print(id(plt.gca()) == id(ax))
# # True





url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS'
vix = pd.read_csv(url, index_col=0, parse_dates=True, na_values='.', infer_datetime_format=True, squeeze=True).dropna()
# `ma` is a 90-day moving average of the VIX Index, a measure of market expectations of near-term stock volatility.
# `state` is a binning of the moving average into different regime states.
ma = vix.rolling('90d').mean()
state = pd.cut(ma, bins=[-np.inf, 14, 18, 24, np.inf], labels=range(4))

# `cmap` is a ColorMap - a matplotlib object that is essentially a mapping of floats to RGBA colors. Any colormap can be reversed by appending '_r'
cmap = plt.get_cmap('RdYlGn_r')
ma.plot(color='black', linewidth=1.5, marker='', figsize=(8, 4), label='VIX 90d MA')
ax = plt.gca()
ax.set_xlabel('')
ax.set_ylabel('90d moving average: CBOE VIX')
ax.set_title('Volatility Regime State')
ax.grid(False)
ax.legend(loc='upper center')
ax.set_xlim(left=ma.index[0], right=ma.index[-1])

# Creates color-filled blocks that correspond to each bin of state.cmap([...])
# Get us an RGBA sequence for the colors at the 20th, 40th, 60th, and 80th ‘percentile’ along the ColorMaps’ spectrum.
trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
for i, color in enumerate(cmap([0.2, 0.4, 0.6, 0.8])):
    ax.fill_between(ma.index, 0, 1, where=state==i, facecolor=color, transform=trans)

# horizontal line
ax.axhline(vix.mean(), linestyle='dashed', color='xkcd:dark grey', alpha=0.6, label='Full-period mean', marker='')
# plt.show()
sf.save_to_file('pandas')