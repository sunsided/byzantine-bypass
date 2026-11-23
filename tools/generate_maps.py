#!/usr/bin/env python3
"""Deterministic, geographically anchored illustrative route maps.

The locations are approximate modern town coordinates. Lines are conceptual
courier routes, not reconstructed 1071 troop movements or verified roads.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon, Rectangle, PathPatch
from matplotlib.path import Path as MplPath
from matplotlib import patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import FontProperties

OUT=Path(__file__).resolve().parent.parent/'assets'
OUT.mkdir(parents=True,exist_ok=True)
# Approximate town-center coordinates (longitude, latitude), not army positions.
PLACES={
 'Bulanık':(42.270,39.092), 'Manzikert':(42.540,39.145),
 'Patnos':(42.867,39.233),'Hınıs':(41.703,39.357),
 'Erzurum':(41.269,39.904),'Horasan':(42.173,40.038),
 'Eleşkirt':(42.678,39.801),'Tutak':(42.773,39.538),
 'Ahlat':(42.482,38.753),'Adilcevaz':(42.729,38.807),
}
# Compute x in approximate local equidistant projection; lat/lon in WGS84.
COS=np.cos(np.deg2rad(39.5))
def xy(lon,lat): return ((lon-40.2)*COS,lat-38.5)
def p(name): return xy(*PLACES[name])

BG='#eee2c3'; INK='#302f28'; MUTED='#766f5d'; RED='#a44e45'; BLUE='#286879'; BLUEH='#154451'; GOLD='#a38851'
font_serif='DejaVu Serif'
font_sans='DejaVu Sans'

# Rough eastern Lake Van northern shoreline. This is illustrative, not survey geometry.
van_boundary=[(42.04,38.50),(42.13,38.58),(42.24,38.60),(42.29,38.65),
 (42.36,38.72),(42.41,38.77),(42.49,38.80),(42.53,38.83),
 (42.61,38.83),(42.69,38.85),(42.74,38.87),(42.82,38.88),
 (42.92,38.94),(43.02,38.96),(43.11,38.94),(43.18,38.97),
 (43.25,38.97),(43.34,38.94),(43.42,38.89),(43.53,38.84),
 (43.66,38.82),(43.83,38.73),(43.83,38.48)]


def smooth_path(coords):
 """Catmull-Rom converted to cubic Bézier, for map drawing (not road routing)."""
 pts=np.array(coords)
 verts=[tuple(pts[0])]; codes=[MplPath.MOVETO]
 for i in range(len(pts)-1):
  p0=pts[i-1] if i else pts[i]
  p1=pts[i]; p2=pts[i+1]
  p3=pts[i+2] if i+2<len(pts) else pts[i+1]
  verts.extend([tuple(p1+(p2-p0)/6), tuple(p2-(p3-p1)/6),tuple(p2)])
  codes.extend([MplPath.CURVE4]*3)
 return MplPath(verts,codes)

def path_draw(ax,nodes,col,lw=4,ls='-',alpha=1,shadow=True,z=12):
 path=smooth_path(nodes)
 if shadow:
  ax.add_patch(PathPatch(path,facecolor='none',edgecolor=BG,lw=lw+5,capstyle='round',joinstyle='round',alpha=.94,zorder=z-1))
 ax.add_patch(PathPatch(path,facecolor='none',edgecolor=col,lw=lw,ls=ls,capstyle='round',joinstyle='round',alpha=alpha,zorder=z))
 return path

def label(ax,txt,x,y,fs=13,weight='normal',col=INK,ha='center',va='center',serif=False,rotation=0,z=20,outline=True):
 t=ax.text(x,y,txt,fontsize=fs,fontfamily=font_serif if serif else font_sans,
        fontweight=weight,color=col,ha=ha,va=va,rotation=rotation,zorder=z)
 if outline: t.set_path_effects([pe.withStroke(linewidth=2.7,foreground=BG,alpha=.90)])
 return t

def place_mark(ax,name,dy=0.0,dx=0.0,fs=11,label_text=None,anchor='left',bold=False):
 x,y=p(name)
 ax.scatter([x],[y],s=23,facecolor='#8d7652',edgecolor=BG,linewidth=1.7,zorder=10)
 o=0.048 if anchor=='left' else -0.048
 label(ax,label_text or name,x+o+dx,y+dy,fs=fs,ha=anchor,col='#655c4b',weight='bold' if bold else 'normal')

def add_text_frame(fig, ax, variant):
 fig.patch.set_facecolor(BG)
 fig.text(.052,.943,'VIA THEODOSIOPOLIS',fontfamily=font_serif,fontsize=29,fontweight='bold',color=INK)
 fig.text(.053,.904,('PLATE I  /  THE PROBLEM' if variant=='problem' else 'PLATE II  /  THE BREAKTHROUGH'),
          fontfamily=font_sans,fontsize=11,fontweight='bold',color=RED if variant=='problem' else BLUE)
 fig.text(.95,.937,'AN ANACHRONISTIC STUDY IN COURIER ROUTING',ha='right',fontfamily=font_sans,
          fontsize=9,color=MUTED)
 fig.add_artist(plt.Line2D([.05,.95],[.882,.882],transform=fig.transFigure,color='#857b5f',lw=1.2))
 fig.add_artist(plt.Line2D([.05,.95],[.105,.105],transform=fig.transFigure,color='#857b5f',lw=1.2))
 fig.text(.052,.077,'FICTIONAL SCENARIO · REAL PLACE NAMES · SCHEMATIC COURIER ROUTES',
          color=MUTED,fontsize=9,fontfamily=font_sans)
 fig.text(.95,.077,'1071 / EASTERN ANATOLIA',color=MUTED,ha='right',fontsize=9,fontfamily=font_sans)


def make(variant):
 np.random.seed(6)
 fig=plt.figure(figsize=(16,9),dpi=150)
 ax=fig.add_axes([.045,.13,.91,.72])
 ax.set_facecolor(BG)
 xmin,xmax=xy(40.15,38.5)[0],xy(43.63,38.5)[0]
 ymin,ymax=xy(40.2,38.44)[1],xy(40.2,40.25)[1]
 ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax)
 ax.set_aspect('auto')
 ax.axis('off')
 add_text_frame(fig,ax,variant)
 # Soft cartographic terrain. Synthetic relief is intentionally non-topographic.
 xx=np.linspace(xmin,xmax,550);yy=np.linspace(ymin,ymax,300)
 X,Y=np.meshgrid(xx,yy)
 relief=(.60*np.sin(X*14+Y*4)*np.cos(Y*11-X*2)+
         .25*np.sin(X*31)*np.cos(Y*23)+.28*np.cos(X*5.4+Y*7))
 rng=np.random.default_rng(1071)
 paper=rng.normal(0,.17,(300,550))+relief*.25
 cmap=LinearSegmentedColormap.from_list('paper',['#bba47b','#e7d4ab','#f1e6cb','#e6d7b7'])
 ax.imshow(paper,extent=[xmin,xmax,ymin,ymax],cmap=cmap,alpha=.24,zorder=0,origin='lower')
 # Relief/contours purely decorative, not geography.
 Z=(np.exp(-((X-xy(41.35,39.8)[0])**2/.30+(Y-1.10)**2/.08))+
    .5*np.exp(-((X-xy(42.9,40.05)[0])**2/.22+(Y-1.4)**2/.12))+
    .16*np.sin(16*X+Y*2)*np.cos(16*Y))
 ax.contour(X,Y,Z,levels=[.13,.22,.32,.43,.54,.68],colors='#8f8a69',alpha=.17,linewidths=.65,zorder=2)
 # Subtle meridian / parallel grid
 for lon in (40.5,41,41.5,42,42.5,43,43.5):
  x=xy(lon,39.5)[0];ax.axvline(x,color='#756d53',lw=.38,alpha=.14,zorder=1)
 for lat in (38.5,39,39.5,40):
  y=xy(41.5,lat)[1];ax.axhline(y,color='#756d53',lw=.38,alpha=.14,zorder=1)
 # Van lake
 lakecoords=[xy(lon,lat) for lon,lat in van_boundary]
 lakecoords.extend([xy(42.04,38.42)])
 ax.add_patch(Polygon(lakecoords,closed=True,facecolor='#b3cbd0',edgecolor='#6e979a',lw=2.3,zorder=4))
 for offset in (.03,.055):
  # fine coastal echo only at NW
  ax.plot([xy(a,b)[0] for a,b in van_boundary[2:17]],
          [xy(a,b)[1]-offset for a,b in van_boundary[2:17]],
          color='#769b9f',lw=.7,alpha=.23,zorder=5)
 label(ax,'LAKE VAN',*xy(43.12,38.70),fs=20,col='#456f7a',weight='bold',serif=True,rotation=-8)
 # faint historical print landmark names
 label(ax,'THE HIGHLANDS OF ARMENIA',*xy(41.55,39.20),fs=15,col='#968665',serif=True,rotation=8)
 # actual town markers
 for name,dy,dx in [('Hınıs',-.08,-.04),('Horasan',.10,.00),('Eleşkirt',.075,.03),('Tutak',.04,.07),('Ahlat',-.075,-.06),('Adilcevaz',-.09,.0)]:
  place_mark(ax,name,dy=dy,dx=dx,fs=9)
 # battlefield zone centered near town, conceptual not historical perimeter
 ex,ey=p('Manzikert')
 for fac,col,alp in [(1.45,'#b56255',.035),(1.12,'#b56255',.07),(1,'#b56255',.12)]:
  ax.add_patch(Ellipse((ex,ey),width=.40*fac*COS,height=.29*fac,angle=14,facecolor=col,
                       edgecolor=RED if fac==1 else 'none',lw=1.4 if fac==1 else 0,
                       linestyle='--' if fac==1 else '-',alpha=alp if fac!=1 else .65,zorder=6))
 label(ax,'CONTESTED GROUND',*xy(42.62,39.49),fs=10,col=RED,weight='bold')
 # stylized battle flags and tents
 for lon,lat in [(42.48,39.09),(42.59,39.17),(42.52,39.19)]:
  x,y=xy(lon,lat)
  ax.plot([x,x],[y-.013,y+.026],color='#8e574f',lw=1.3,zorder=8)
  ax.add_patch(Polygon([[x,y+.026],[x+.026,y+.019],[x,y+.009]],closed=True,
                       facecolor=RED,edgecolor=INK,lw=.35,zorder=8))
 place_mark(ax,'Manzikert',dy=-.15,dx=.11,fs=13,bold=True)
 a=p('Bulanık');b=p('Patnos')
 # general encampments as decorative markers outside danger zone
 for name,point,side in [('A',a,-1),('B',b,1)]:
  x,y=point
  ax.add_patch(Circle((x,y),.054,facecolor=BG,edgecolor='#5d513b',lw=2,zorder=13))
  ax.add_patch(Polygon([[x-.019,y-.014],[x,y+.03],[x+.019,y-.014]],facecolor='#796e50',edgecolor=INK,lw=1,zorder=14))
  label(ax,name,x,y-.002,fs=7,weight='bold',col=BG,outline=False,z=15)
 if variant=='problem':
  # courier crosses contested ground and gets intercepted
  stop=xy(42.482,39.145)
  path_draw(ax,[a,xy(42.39,39.11),stop],RED,lw=4.4,ls=(0,(9,6)),z=15)
  path_draw(ax,[stop,xy(42.69,39.205),b],RED,lw=2.0,ls=(0,(2,8)),alpha=.42,z=12,shadow=False)
  x,y=stop
  ax.plot([x-.045,x+.045],[y-.044,y+.044],color=RED,lw=5,zorder=24)
  ax.plot([x-.045,x+.045],[y+.044,y-.044],color=RED,lw=5,zorder=24)
  label(ax,'INTERCEPTED',*xy(42.24,39.42),fs=12,col=RED,weight='bold',ha='center')
  ax.plot([x,xy(42.32,39.37)[0]],[y,xy(42.32,39.37)[1]],color=RED,lw=1.2,alpha=.75,zorder=19)
  label(ax,'The courier never arrives.',*xy(41.31,38.83),fs=12,col=RED,serif=True,rotation=-3)
  label(ax,'DIRECT ROUTE',*xy(42.20,39.25),fs=10,col=RED,weight='bold')
 else:
  # faded version of the unsuccessful route is shown for direct comparison
  path_draw(ax,[a,xy(42.46,39.135),b],RED,lw=1.8,ls=(0,(2,7)),alpha=.52,z=9,shadow=False)
  nodes=[a,xy(42.08,39.19),p('Hınıs'),xy(41.47,39.65),p('Erzurum'),
         xy(41.72,40.1),p('Horasan'),p('Eleşkirt'),p('Tutak'),b]
  path_draw(ax,nodes,BLUEH,lw=7.5,alpha=.95,z=15)
  path_draw(ax,nodes,BLUE,lw=3.9,z=16,shadow=False)
  # arrow heads on two segments
  for (lon1,lat1),(lon2,lat2) in [((41.72,40.1),(41.84,40.09)),((42.735,39.65),(42.755,39.61))]:
   ax.add_patch(FancyArrowPatch(xy(lon1,lat1),xy(lon2,lat2),arrowstyle='-|>',mutation_scale=20,
                                lw=1,facecolor='#e3d6b5',edgecolor='#e3d6b5',zorder=19))
  exr,eyr=p('Erzurum')
  ax.scatter([exr],[eyr],s=270,facecolor='#d5b76c',edgecolor=BLUEH,lw=2.2,zorder=22)
  label(ax,'THEODOSIOPOLIS',exr,eyr-.12,fs=15,col=BLUEH,weight='bold',serif=True)
  label(ax,'(modern Erzurum)',exr,eyr-.19,fs=10,col=MUTED)
  label(ax,'DESIGNATED SAFE RELAY*',*xy(41.20,40.165),fs=11,col=BLUEH,weight='bold')
  label(ax,'THE LONG WAY AROUND',*xy(42.00,40.215),fs=11,col=BLUE,weight='bold')
  # emphasize successful receipt
  xb,yb=b
  ax.add_patch(Circle((xb,yb),.093,edgecolor=BLUE,facecolor='none',linewidth=2.2,zorder=19))
  label(ax,'DELIVERED',*xy(43.12,39.43),fs=12,col=BLUEH,weight='bold')
  label(ax,'*Safe according to the route planner. Historicity not guaranteed.',*xy(41.1,38.69),fs=9,col=BLUEH,ha='left',serif=True)
 # town names near generals
 place_mark(ax,'Bulanık',dy=-.108,dx=-.09,fs=10,bold=True)
 label(ax,'GENERAL A',*xy(42.12,39.26),fs=11,weight='bold')
 place_mark(ax,'Patnos',dy=-.125,dx=.03,fs=10,bold=True)
 label(ax,'GENERAL B',*xy(43.12,39.27),fs=11,weight='bold')
 # compass in corner, decorative consistent on both
 cx,cy=xy(40.51,39.91)
 for i,(sx,sy) in enumerate([(0,.11),(.11,0),(0,-.11),(-.11,0)]):
  col=INK if i==0 else '#a89a77'
  ax.plot([cx,cx+sx],[cy,cy+sy],color=col,lw=1.6,zorder=8)
 label(ax,'N',cx,cy+.16,fs=13,col=INK,serif=True,weight='bold')
 ax.add_patch(Circle((cx,cy),.018,facecolor=INK,zorder=9))
 # scale bar approximate local km
 base=xy(40.48,38.66)
 km_lon=50/(111.2*COS)
 sx=km_lon*COS
 ax.plot([base[0],base[0]+sx],[base[1],base[1]],color=INK,lw=3,zorder=25)
 ax.plot([base[0],base[0]],[base[1]-.015,base[1]+.015],color=INK,lw=1.3,zorder=25)
 ax.plot([base[0]+sx,base[0]+sx],[base[1]-.015,base[1]+.015],color=INK,lw=1.3,zorder=25)
 label(ax,'~50 km',base[0]+sx/2,base[1]+.06,fs=9,col=MUTED)
 # export
 fn='01-intercepted' if variant=='problem' else '02-detour'
 fig.savefig(OUT/f'{fn}.png',dpi=160,facecolor=BG)
 fig.savefig(OUT/f'{fn}.svg',facecolor=BG)
 plt.close(fig)

if __name__=='__main__':
 make('problem');make('solution')
