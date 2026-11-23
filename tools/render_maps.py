# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "basemap", "basemap-data-hires"]
# ///
"""Generate two geographically matching, fictional Manzikert-themed campaign maps.

Modern coastlines are geographic reference only; neither deployments nor routes
are historical reconstructions. Map rendering uses Basemap's GSHHS coastline data.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, FancyArrowPatch
from matplotlib import patheffects as pe
from mpl_toolkits.basemap import Basemap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)

INK = '#282922'
MUTED = '#766B55'
PARCHMENT = '#F4EAD2'
LAND = '#E6D5A9'
SEA = '#C6D4D0'
COAST = '#8B826C'
BAD = '#B4483B'
GOOD = '#24766A'
GOLD = '#A87F33'

CITIES = {
    'Constantinople': (28.9784, 41.0082),
    'Ankara': (32.8597, 39.9334),
    'Sebasteia': (37.015, 39.748),  # modern Sivas
    'Trebizond': (39.720, 41.001), # modern Trabzon
    'Kars': (43.0975, 40.6013),
    'Manzikert': (42.540, 39.145), # modern Malazgirt
}
A = (42.11, 39.29)
B = (42.91, 39.29)
D = (42.53, 39.45)
AMBUSH = (42.53, 39.29)

plt.rcParams.update({
    'font.family': 'DejaVu Serif',
    'font.size': 12,
    'svg.fonttype': 'path',  # viewers lack DejaVu; live text would reflow labels
    'savefig.facecolor': PARCHMENT,
})

def text(ax, x, y, s, *, size=11, color=INK, weight='normal', ha='left', va='center', rotation=0, z=25, alpha=1, style='normal', halo=True):
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                   ha=ha, va=va, rotation=rotation, zorder=z, alpha=alpha,
                   fontstyle=style,
                   path_effects=[pe.withStroke(linewidth=2.5, foreground=PARCHMENT, alpha=.80)] if halo else [])

def basemap_on(ax, bounds, detail='i'):
    m = Basemap(projection='cyl', llcrnrlon=bounds[0], llcrnrlat=bounds[1],
                urcrnrlon=bounds[2], urcrnrlat=bounds[3], resolution=detail, ax=ax)
    ax.set_facecolor(SEA)
    m.fillcontinents(color=LAND, lake_color=SEA, zorder=1)
    m.drawcoastlines(color=COAST, linewidth=.8, zorder=3)
    m.drawmapboundary(color=INK, linewidth=1.2, fill_color=SEA)
    for lon in np.arange(28,46,2):
        ax.plot([lon,lon], [bounds[1],bounds[3]], color=COAST, lw=.45, alpha=.18, zorder=2)
    for lat in np.arange(36,45,2):
        ax.plot([bounds[0],bounds[2]], [lat,lat], color=COAST, lw=.45, alpha=.18, zorder=2)
    ax.set_xlim(bounds[0],bounds[2]);ax.set_ylim(bounds[1],bounds[3])
    ax.set_aspect('auto')
    ax.set_xticks([]);ax.set_yticks([])
    return m

def dot(ax, p, color=INK, radius=4, z=17):
    ax.plot(*p, marker='o', color=PARCHMENT, markersize=radius+4, zorder=z)
    ax.plot(*p, marker='o', color=color, markersize=radius, zorder=z+1)

def march(ax, nodes, *, color=GOOD, linewidth=3.7, dash=None, alpha=1, z=15, arrow=True):
    xs = [a[0] for a in nodes]; ys=[a[1] for a in nodes]
    ax.plot(xs,ys,color=PARCHMENT,lw=linewidth+3, solid_joinstyle='round',
            solid_capstyle='round',alpha=.96,zorder=z-1)
    ax.plot(xs,ys,color=color,lw=linewidth,ls=dash or '-',
            solid_joinstyle='round',solid_capstyle='round',alpha=alpha,zorder=z)
    if arrow and len(nodes)>=2:
        s,e=nodes[-2],nodes[-1]
        frac=.20
        start=(e[0]*(1-frac)+s[0]*frac, e[1]*(1-frac)+s[1]*frac)
        ax.add_patch(FancyArrowPatch(start,e,arrowstyle='-|>',mutation_scale=18,
                color=color,linewidth=0,zorder=z+2))

def border_decor(fig, number, subtitle, title):
    fig.patch.set_facecolor(PARCHMENT)
    fig.text(.055,.94,'THE BYZANTINE BYPASS  /  MILITARY LOGISTICS RESEARCH SERIES',
             fontsize=13,color=MUTED, fontweight='bold')
    fig.text(.947,.94,number, fontsize=13,color=MUTED,ha='right')
    fig.text(.055,.865,title,fontsize=29,color=INK,fontweight='bold')
    fig.text(.055,.825,subtitle,fontsize=14,color=MUTED)
    fig.add_artist(plt.Line2D([.055,.947],[.806,.806],transform=fig.transFigure,
                              color=GOLD,lw=1.4))
    fig.add_artist(plt.Line2D([.055,.947],[.116,.116],transform=fig.transFigure,
                              color=GOLD,lw=1.2))
    fig.text(.055,.08,'GEOGRAPHY: REAL  |  DEPLOYMENTS, INTERCEPTIONS & ROUTES: FICTIONAL',
             fontsize=9.3,color=MUTED)
    fig.text(.947,.08,'NOT TO SCALE IN TIME OR HORSEPOWER',fontsize=9.3,color=MUTED,ha='right')

def citylabels(ax):
    dot(ax,CITIES['Constantinople'],INK,4)
    text(ax,29.15,40.70,'CONSTANTINOPLE',size=10,weight='bold')
    dot(ax,CITIES['Trebizond'],INK,3)
    text(ax,39.72,40.74,'Trebizond',size=10,ha='center')
    dot(ax,CITIES['Sebasteia'],INK,3)
    text(ax,36.82,39.36,'Sebasteia',size=10,ha='center')
    dot(ax,CITIES['Ankara'],INK,3)
    text(ax,32.95,39.56,'Ancyra',size=10)
    dot(ax,CITIES['Kars'],INK,3)
    text(ax,43.25,40.75,'Kars',size=10)
    text(ax,34.0,42.75,'P O N T U S   E U X I N U S   ( B L A C K   S E A )',
         size=10.5,color='#476E70',ha='center',style='italic')
    text(ax,35.1,37.23,'A  N  A  T  O  L  I  A',size=19,color='#877653',ha='center',alpha=.65)
    text(ax,43.1,38.15,'Lake Van',size=10,color='#547F83',ha='center',style='italic')

def battlemark(ax):
    ax.add_patch(Circle((42.54,39.25),.66, color=BAD,alpha=.115,zorder=6,lw=0))
    ax.add_patch(Circle((42.54,39.25),.66, fill=False,ec=BAD,lw=1.4,
                        ls=(0,(5,4)),alpha=.65,zorder=7))
    dot(ax,CITIES['Manzikert'],BAD,4)
    text(ax,41.95,38.72,'MANZIKERT 1071',size=11,color=BAD,weight='bold',ha='right')

def mini(ax, mode):
    basemap_on(ax,(41.85,38.95,43.17,39.72),'i')
    ax.add_patch(Circle((42.53,39.29),.25,color=BAD,alpha=.13,zorder=7))
    ax.add_patch(Circle((42.53,39.29),.25,fill=False,ls='--',ec=BAD,lw=1.3,zorder=8))
    if mode=='problem':
        march(ax,[A,B],color=BAD,linewidth=3.8,dash='--',arrow=False)
        ax.plot(*AMBUSH,marker='X',color=BAD,markersize=17,mew=2.8,zorder=18)
        text(ax,42.53,39.06,'INTERCEPTED',size=11,ha='center',color=BAD,weight='bold')
    else:
        march(ax,[A,(41.91,39.58)],color=GOOD,linewidth=3.4,arrow=True)
        march(ax,[(42.98,39.69),B],color=GOOD,linewidth=3.4,arrow=True)
        text(ax,42.54,39.12,'NO MESSENGER HERE',size=9,ha='center',color=GOOD,weight='bold')
    for p,code in [(A,'A'),(B,'B')]:
        ax.scatter(*p,s=210,facecolor=INK,edgecolor=PARCHMENT,linewidth=2,zorder=22)
        text(ax,p[0],p[1],code,size=10,color='white',weight='bold',ha='center',z=23,halo=False)
    # The excluded general is a purely fictional extra character.
    ax.scatter(*D,s=195,facecolor=BAD,edgecolor=PARCHMENT,linewidth=1.7,zorder=22)
    text(ax,*D,'D',size=10,color='white',weight='bold',ha='center',z=23,halo=False)
    if mode=='solution':
        ax.plot([42.44,42.62],[39.35,39.55],lw=3.5,color=BAD,zorder=24)
        ax.plot([42.44,42.62],[39.55,39.35],lw=3.5,color=BAD,zorder=24)
        text(ax,42.53,39.66,'DO NOT CC',size=10,color=BAD,weight='bold',ha='center')
    else:
        text(ax,42.53,39.66,'UNTRUSTED D',size=10,color=BAD,ha='center')
    ax.set_title('BATTLEFIELD DETAIL',loc='left',pad=11,color=INK,fontsize=12,fontweight='bold')

def render(mode):
    fig=plt.figure(figsize=(16,9),dpi=170)
    is_sol=mode=='solution'
    border_decor(fig, 'PLATE II / II' if is_sol else 'PLATE I / II',
      'A proposed topological intervention in late-Roman message delivery.' if is_sol
      else 'An avoidable communication issue near a contested region.',
      'II. The Long Way Around' if is_sol else 'I. The Problem')
    ax=fig.add_axes([.055,.175,.682,.588])
    basemap_on(ax,(26.8,36.45,45.0,43.50),'i')
    citylabels(ax)
    battlemark(ax)
    if is_sol:
        land_west=[A,(40.2,39.79),CITIES['Sebasteia'],CITIES['Ankara'],
                   (30.73,40.14),CITIES['Constantinople']]
        sea_leg=[CITIES['Constantinople'],(29.75,41.7),(32.2,42.2),(35.1,42.1),
                 (38.2,41.6),CITIES['Trebizond']]
        land_east=[CITIES['Trebizond'],(41.22,40.81),CITIES['Kars'],
                   (43.08,39.9),B]
        march(ax,land_west,color=GOOD,linewidth=3.7)
        march(ax,sea_leg,color='#276791',linewidth=3.7,dash='--')
        march(ax,land_east,color=GOOD,linewidth=3.7)
        text(ax,33.4,41.75,'OPTIMIZED SEA LEG',size=10,color='#276791',weight='bold',ha='center',rotation=4)
        text(ax,33.1,39.24,'A SLIGHT DETOUR',size=11,color=GOOD,weight='bold',rotation=5)
        text(ax,41.5,41.2,'THE SAFE WAY BACK',size=10,color=GOOD,weight='bold',rotation=-6,ha='center')
        dot(ax,CITIES['Constantinople'],GOLD,6)
        dot(ax,CITIES['Trebizond'],GOLD,6)
    else:
        march(ax,[A,B],color=BAD,linewidth=3.7,dash='--',arrow=False)
        ax.plot(*AMBUSH,marker='X',color=BAD,markersize=13,mew=2.8,zorder=18)
        text(ax,41.8,39.13,'MESSENGER LOST',size=10,color=BAD,weight='bold',ha='right')
        # an intentionally unused safe alternate route, as a visual tease
        text(ax,32.7,41.42,'A WHOLE EMPIRE OF AVAILABLE ROADS',size=10,color=MUTED,style='italic')
    ax.set_title('ANATOLIA, 1071  /  MODERN COASTLINE GEOGRAPHY',loc='left',pad=11,color=INK,fontsize=12,fontweight='bold')
    inset=fig.add_axes([.764,.413,.183,.35])  # top aligned with main map
    mini(inset,mode)
    side=fig.add_axes([.764,.155,.183,.208]);side.axis('off')
    side.add_patch(Rectangle((0,.01),1,.96,fill=False,ec=COAST,lw=1.1,transform=side.transAxes))
    side.text(.08,.86,'PROTOCOL FINDING',fontsize=11,color=GOLD,fontweight='bold',transform=side.transAxes)
    if is_sol:
        side.text(.08,.68,'1. AVOID THE BATTLEFIELD',fontsize=9.6,color=GOOD,transform=side.transAxes,fontweight='bold')
        side.text(.08,.49,'2. AVOID GENERAL D',fontsize=9.6,color=GOOD,transform=side.transAxes,fontweight='bold')
        side.text(.08,.24,'Consensus achieved*',fontsize=13,color=INK,transform=side.transAxes,fontweight='bold')
        side.text(.08,.10,'* not independently verified',fontsize=8.6,color=MUTED,transform=side.transAxes)
    else:
        side.text(.08,.68,'MESSAGE DELIVERED:',fontsize=10,color=INK,transform=side.transAxes)
        side.text(.08,.45,'NO',fontsize=29,color=BAD,transform=side.transAxes,fontweight='bold')
        side.text(.08,.19,'GENERAL D: SUSPICIOUS',fontsize=9.7,color=BAD,transform=side.transAxes,fontweight='bold')
    p=OUT/('02-the-long-way-around' if is_sol else '01-the-problem')
    fig.savefig(str(p)+'.png',dpi=170,bbox_inches=None)
    fig.savefig(str(p)+'.svg',bbox_inches=None)
    plt.close(fig)
    print(p)

if __name__ == '__main__':
    render('problem')
    render('solution')
