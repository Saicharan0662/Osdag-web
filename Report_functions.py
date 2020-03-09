from builtins import str
import time
import math
# from Common import *
import os
import pdfkit
import configparser
# from utils.common import component
from pylatex import Document, Section, Subsection
from pylatex.utils import italic, bold
import pdflatex
import sys
import datetime
from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject


from pylatex import Document, Section, Subsection, Tabular, Tabularx,MultiColumn
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic, NoEscape
from pdflatex import PDFLaTeX
import os
from pylatex import Document, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number
from pylatex.utils import bold

def min_pitch_req(d,t):
    min_pitch = 2.5*d
    max_pitch_1 = 32*min(t)
    max_pitch_2 = 300
    max_pitch = max(max_pitch_1,max_pitch_2)
    d = str(d)
    t = str(min(t))
    max_pitch_1 = str(max_pitch_1)
    max_pitch_2 = str(max_pitch_2)
    max_pitch = str(max_pitch)
    min_pitch = str(min_pitch)

    min_pitch_eqn = Math(inline=True)
    min_pitch_eqn.append(NoEscape(r'\begin{aligned} min.~ pitch/gauge &= 2.5 ~ d\\'))
    min_pitch_eqn.append(NoEscape(r'&= 2.5*' + d + r'=' + min_pitch + r'\\'))
    min_pitch_eqn.append(NoEscape(r'max.~ pitch/gauge &=\min(32~t,~300~mm)\\'))
    min_pitch_eqn.append(NoEscape(r' &= \min(32 *~' + t+ r',~ 300 ~mm)='+max_pitch+r'\end{aligned}'))
    return min_pitch_eqn

def min_edge_end_req(d_0,edge_type,f_y,t):
    if edge_type == 'hand_flame_cut':
        factor = 1.7
    else:
        factor = 1.5
    min_edge_dist = round(factor * d_0,2)
    epsilon = round(math.sqrt(250/f_y),2)
    max_edge_dist = round(12*t*epsilon,2)

    min_edge_dist = str(min_edge_dist)
    max_edge_dist = str(max_edge_dist)
    t = str(t)
    f_y = str(f_y)
    epsilon = str(epsilon)
    factor = str(factor)
    d_0 = str(d_0)

    min_end_edge_eqn = Math(inline=True)
    min_end_edge_eqn.append(NoEscape(r'\begin{aligned} min.~ end/edge &= [1.5~or~ 1.7] * d_0\\'))
    min_end_edge_eqn.append(NoEscape(r'&= '+factor + r'*' + d_0+r'='+min_edge_dist+r'\\'))
    min_end_edge_eqn.append(NoEscape(r'max.~ end/edge &=12~ t~ \varepsilon\\'))
    min_end_edge_eqn.append(NoEscape(r'\varepsilon &= \sqrt{\frac{250}{f_y}}\\'))
    min_end_edge_eqn.append(NoEscape(r'max.~ end/edge&=12 ~*'+ t + r'*\sqrt{\frac{250}{'+f_y+r'}}\\ &='+max_edge_dist+r'\\ \end{aligned}'))
    return min_end_edge_eqn

def bolt_shear_prov(f_ub,n_n,a_nb,gamma_mb,bolt_shear_capacity):
    f_ub = str(f_ub)
    n_n = str(n_n)
    a_nb = str(a_nb)
    gamma_mb= str(gamma_mb)
    bolt_shear_capacity=str(bolt_shear_capacity)
    bolt_shear_eqn = Math(inline=True)
    bolt_shear_eqn.append(NoEscape(r'\begin{aligned}V_{dsb} &= \frac{f_ub ~n_n~ A_{nb}}{\sqrt{3} ~\gamma_{mb}}\\'))
    bolt_shear_eqn.append(NoEscape(r'&= \frac{'+f_ub+'*'+n_n+'*'+a_nb+'}{\sqrt{3}~*~'+ gamma_mb+r'}\\'))
    bolt_shear_eqn.append(NoEscape(r'&= '+bolt_shear_capacity+r'\end{aligned}'))
    return bolt_shear_eqn

def bolt_bearing_prov(k_b,d,conn_plates_t_fu_fy,gamma_mb,bolt_bearing_capacity):
    t_fu_prev = conn_plates_t_fu_fy[0][0] * conn_plates_t_fu_fy[0][1]
    t = conn_plates_t_fu_fy[0][0]
    f_u = conn_plates_t_fu_fy[0][1]
    for i in conn_plates_t_fu_fy:
        t_fu = i[0] * i[1]
        if t_fu <= t_fu_prev:
            t = i[0]
            f_u = i[1]
    k_b = str(k_b)
    d = str(d)
    t = str(t)
    f_u= str(f_u)
    gamma_mb=str(gamma_mb)
    bolt_bearing_capacity = str(bolt_bearing_capacity)
    bolt_bearing_eqn = Math(inline=True)
    bolt_bearing_eqn.append(NoEscape(r'\begin{aligned}V_{dpb} &= \frac{2.5~ k_b~ d~ t~ f_u}{\gamma_{mb}}\\'))
    bolt_bearing_eqn.append(NoEscape(r'&= \frac{2.5~*'+ k_b+'*'+ d+'*'+t+'*' +'*'+f_u+'}{'+gamma_mb+r'}\\'))
    bolt_bearing_eqn.append(NoEscape(r'&='+bolt_bearing_capacity+r'\end{aligned}'))

    return bolt_bearing_eqn


def bolt_capacity_prov(bolt_shear_capacity,bolt_bearing_capacity,bolt_capacity):
    bolt_shear_capacity = str(bolt_shear_capacity)
    bolt_bearing_capacity = str(bolt_bearing_capacity)
    bolt_capacity = str(bolt_capacity)
    bolt_capacity_eqn = Math(inline=True)
    bolt_capacity_eqn.append(NoEscape(r'\begin{aligned}V_{db} &= min~ (V_{dsb}, V_{dpb})\\'))
    bolt_capacity_eqn.append(NoEscape(r'&= min~ ('+bolt_shear_capacity+','+ bolt_bearing_capacity+r')\\'))
    bolt_capacity_eqn.append(NoEscape(r'&='+ bolt_capacity+r'\end{aligned}'))

    return bolt_capacity_eqn


def HSFG_bolt_capacity_prov(mu_f,n_e,K_h,fub,Anb,gamma_mf,capacity):
    mu_f = str(mu_f)
    n_e = str(n_e)
    K_h = str(K_h)
    fub = str(fub)
    Anb = str(Anb)
    gamma_mf = str(gamma_mf)
    capacity = str(capacity)

    HSFG_bolt_capacity_eqn = Math(inline=True)
    HSFG_bolt_capacity_eqn.append(NoEscape(r'\begin{aligned}V_{dsf} & = \frac{\mu_f~ n_e~  K_h~ F_o}{\gamma_{mf}}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'& Where, F_o = 0.7 * f_{ub} A_{nb}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'V_{dsf} & = \frac{'+ mu_f + '*' + n_e + '*' + K_h +'* 0.7 *' +fub+'*'+Anb +r'}{'+gamma_mf+r'}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'& ='+capacity+r'\end{aligned}'))

    return HSFG_bolt_capacity_eqn

def get_trial_bolts(V_u, A_u,bolt_capacity):
    res_force = math.sqrt(V_u**2+ A_u**2)
    trial_bolts = math.ceil(res_force/bolt_capacity)
    V_u=str(V_u)
    A_u=str(A_u)
    bolt_capacity=str(bolt_capacity)
    trial_bolts=str(trial_bolts)
    trial_bolts_eqn = Math(inline=True)
    trial_bolts_eqn.append(NoEscape(r'\begin{aligned}R_{u} &= \sqrt{V_u^2+A_u^2}\\'))
    trial_bolts_eqn.append(NoEscape(r'n_{trial} = R_u/ V_{bolt}\\'))
    trial_bolts_eqn.append(NoEscape(r'& = \frac{\sqrt{'+V_u+r'^2+'+A_u+r'^2}}{'+bolt_capacity+ r'}\\'))
    trial_bolts_eqn.append(NoEscape(r'& ='+trial_bolts+ r'\end{aligned}'))
    return trial_bolts_eqn

def get_pass_fail(required, provided):
    required = float(required)
    provided = float(provided)
    if required < provided:
        return 'Pass'
    else:
        return 'Fail'


    # doc.generate_pdf('report_functions', clean_tex=False)


# geometry_options = {"top": "2in", "bottom": "1in", "left": "0.6in", "right": "0.6in", "headsep": "0.8in"}
# doc = Document(geometry_options=geometry_options, indent=False)
# report_bolt_shear_check(doc)