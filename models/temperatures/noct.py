#------------------------------------------------------------------------------
def t_noct(ta_list, poa_irrad_list, NOCT):
    t_noct_list = []
    for ta, poa in zip(ta_list, poa_irrad_list):
        Tc = ta + ((NOCT-20)/800)*poa
        t_noct_list.append(Tc)
    return t_noct_list