class CalculationValidationError(Exception):
    """Ошибка валидации входных данных для расчёта."""

# ------------------------------------------------------------------
# Расчет нулевых значений, также расчет значений на пред. день
# ------------------------------------------------------------------ 
def day_zero_calc(
    V_tstn_rn_vn_0, V_tstn_skn_0, V_tstn_vo_0, V_tstn_tng_0, V_tstn_kchng_0, V_upn_suzun_0, V_suzun_vslu_0, V_suzun_tng_0, V_upsv_yu_0, V_upsv_s_0, 
    V_cps_0, V_gnps_0, V_nps_1_0, V_nps_2_0, V_knps_0, V_tstn_suzun_vankor_0, V_suzun_0, V_tstn_suzun_vslu_0, V_tstn_tagul_0, V_tstn_lodochny_0,
    ):
    V_suzun_slu_0 = V_upn_suzun_0 - V_suzun_vslu_0 - V_suzun_tng_0
    V_cppn_1_0 = V_upsv_yu_0 + V_upsv_s_0 + V_cps_0
    V_tstn_0 = V_gnps_0 + V_nps_1_0 + V_nps_2_0 + V_knps_0
    V_tstn_suzun_0 = V_suzun_0 - V_tstn_suzun_vankor_0 - V_tstn_suzun_vslu_0
    V_tstn_tagul_obsh_0 = V_tstn_tagul_0 + V_tstn_lodochny_0
    V_tstn_vn_0 = (
        V_tstn_0
        - V_tstn_rn_vn_0
        - V_tstn_suzun_0
        - V_tstn_tagul_obsh_0
        - V_tstn_skn_0
        - V_tstn_vo_0
        - V_tstn_tng_0
        - V_tstn_kchng_0
    )
    return{
        "V_cppn_1_0":V_cppn_1_0,
        "V_suzun_slu_0":V_suzun_slu_0,
        "V_tstn_0":V_tstn_0,
        "V_tstn_suzun_0":V_tstn_suzun_0,
        "V_tstn_tagul_obsh_0":V_tstn_tagul_obsh_0,
        "V_tstn_vn_0":V_tstn_vn_0,
    }
def prev_day_calc(
    V_upn_suzun_prev, V_upn_lodochny_prev, V_tagul_tr_prev, V_upsv_yu_prev, V_upsv_s_prev, V_cps_prev, V_nps_1_prev, V_nps_2_prev, V_tstn_rn_vn_prev,
    V_upsv_yu, V_upsv_s, V_cps, V_upn_suzun, V_upn_lodochny, V_tagul_tr
    ):       
    if not V_upn_suzun:
        V_upn_suzun = V_upn_suzun_prev
    if not V_upn_lodochny:
        V_upn_lodochny = V_upn_lodochny_prev
    if not V_tagul_tr:
        V_tagul_tr = V_tagul_tr_prev
    if not V_upsv_yu:
        V_upsv_yu = V_upsv_yu_prev
    if not V_upsv_s:
        V_upsv_s = V_upsv_s_prev
    if not V_cps:
        V_cps = V_cps_prev
    V_nps_1 = V_nps_1_prev
    V_nps_2 = V_nps_2_prev
    V_tstn_rn_vn = V_tstn_rn_vn_prev
    return{
        "V_upn_suzun":V_upn_suzun,
        "V_upn_lodochny":V_upn_lodochny,
        "V_tagul_tr":V_tagul_tr,
        "V_upsv_yu":V_upsv_yu,
        "V_upsv_s":V_upsv_s,
        "V_cps":V_cps,
        "V_nps_1":V_nps_1,
        "V_nps_2":V_nps_2,
        "V_tstn_rn_vn":V_tstn_rn_vn,
    }
# ------------------------------------------------------------------
# Блок расчета значений для пересчета
# ------------------------------------------------------------------
def lodochny_upsv_yu_calc(Q_lodochny, K_delta_g_upn_lodochny, K_otkachki, G_lodochny_upsv_yu_month_prev, day, N,
                          Q_tagul):

    G_lodochny_upsv_yu = Q_lodochny * (1 - K_otkachki) - K_delta_g_upn_lodochny / 2
    G_lodochny_upsv_yu_month = float(G_lodochny_upsv_yu_month_prev or 0) + G_lodochny_upsv_yu
    Q_tagul_month = Q_tagul.sum()
    # по умолчанию без предупреждения
    K_otkachki_out = {
        "value": K_otkachki,
        "status": 0,
        "message": None,
    }
    # рассчитывается только на последний день месяца (day == N)
    K_otkachki_month = None
    if day == N:
        K_otkachki_month = G_lodochny_upsv_yu_month / Q_tagul_month
        if abs(K_otkachki - K_otkachki_month) >= 0.01:
            K_otkachki = {
                "value": K_otkachki,
                "status": 3,
                "message": (
                    f"коэффициент откачки K_otkachki={K_otkachki:.4f} "
                    f"не совпадает с расчетным {K_otkachki_month:.4f} (расхождение > 0.01)"
                )
            }

    return {
        "G_lodochny_upsv_yu": G_lodochny_upsv_yu,
        "G_lodochny_upsv_yu_month": G_lodochny_upsv_yu_month,
        "K_otkachki": K_otkachki,
        "Q_tagul_month": Q_tagul_month,
        "K_otkachki_month": K_otkachki_month,
    }
def precalc_value(
        Q_vslu, V_suzun_vslu_prev, V_suzun_tng_prev, G_payaha, G_suzun_tng, Q_vo, G_ichem, V_ichem_prev, G_lodochny_upsv_yu_month,
        Q_tagul, V_tagul_tr_prev, V_tagul_tr, K_delta_g_tagul, Q_kchng, N, G_buying_oil_month, G_out_udt_month, G_sikn_tagul, day,
        V_lodochny_cps_upsv_yu_prev, G_lodochny_upsv_yu, V_suzun_vslu, G_sikn_tagul_manual_entries
):
    G_suzun_vslu = Q_vslu
    V_suzun_tng = G_payaha + V_suzun_tng_prev - G_suzun_tng
    if not V_suzun_vslu:
        V_suzun_vslu = V_suzun_vslu_prev + Q_vslu - G_suzun_vslu
    G_upn_lodochny_ichem = Q_vo
    V_ichem = V_ichem_prev + G_upn_lodochny_ichem - G_ichem
    
    G_tagul = Q_tagul - (V_tagul_tr - V_tagul_tr_prev) - K_delta_g_tagul
    G_kchng = Q_kchng
    G_buying_oil = G_buying_oil_month/N
    G_out_udt = G_out_udt_month/N
    G_per = G_buying_oil - G_out_udt
    G_sikn_tng = G_suzun_tng
    delta_G_tagul = Q_tagul - G_tagul - (V_tagul_tr - V_tagul_tr_prev)
    G_sikn_tagul_is_manual = G_sikn_tagul is not None
    if G_sikn_tagul is None:
        base = round(G_lodochny_upsv_yu_month / N / 10) * 10
        # Определяем 2 последних дня без ручного ввода (остаточные дни)
        remainder_days = []
        for d in range(N, 0, -1):
            if d not in G_sikn_tagul_manual_entries:
                remainder_days.append(d)
            if len(remainder_days) == 2:
                break
        if day in set(remainder_days):
            manual_sum = sum(G_sikn_tagul_manual_entries.values())
            base_count = N - len(G_sikn_tagul_manual_entries) - len(remainder_days)
            remainder = (G_lodochny_upsv_yu_month - base * base_count - manual_sum) / len(remainder_days)
            if remainder >= 900:
                G_sikn_tagul = remainder
            elif day == remainder_days[0]:
                G_sikn_tagul = G_lodochny_upsv_yu_month - base * (base_count + 1) - manual_sum
            else:
                G_sikn_tagul = base
        else:
            G_sikn_tagul = base

    if not (900 <= G_sikn_tagul <= 1500):
        G_sikn_tagul = {
            "value": G_sikn_tagul,
            "status": 3,
            "message": (
                f"откачка нефти на СИКН-1208 вне допустимой вилки (900 … 1500) т "
                f"(текущее {G_sikn_tagul:.2f})"
            ),
        }
    else:
        G_sikn_tagul = {
            "value": G_sikn_tagul,
            "status": 1,
            "message": (None),
            }
    
    V_lodochny_cps_upsv_yu = V_lodochny_cps_upsv_yu_prev + G_lodochny_upsv_yu - G_sikn_tagul['value']
    return {
        "G_suzun_vslu":G_suzun_vslu,
        "V_suzun_tng":V_suzun_tng,
        "V_suzun_vslu":V_suzun_vslu,
        "G_upn_lodochny_ichem":G_upn_lodochny_ichem,
        "V_ichem":V_ichem,
        "G_tagul":G_tagul,
        "G_kchng":G_kchng,
        "G_buying_oil":G_buying_oil,
        "G_out_udt":G_out_udt,
        "G_per":G_per,
        "G_sikn_tng":G_sikn_tng,
        "G_sikn_tagul":G_sikn_tagul,
        "G_sikn_tagul_is_manual":G_sikn_tagul_is_manual,
        "delta_G_tagul":delta_G_tagul,
        "V_lodochny_cps_upsv_yu":V_lodochny_cps_upsv_yu,
    }

# ------------------------------------------------------------------
# Блок пересчета значений
# ------------------------------------------------------------------
def value_recalculation (
        V_upn_suzun, V_upn_suzun_prev, V_suzun_vslu, V_suzun_tng, Q_suzun, Q_vslu, K_delta_g_suzun, G_suzun_vslu, G_suzun_tng, G_payaha, V_suzun_slu_prev,
        V_upn_lodochny, V_ichem, Q_lodochny, Q_vo, G_lodochny_upsv_yu, K_otkachki, V_upn_lodochny_prev, K_delta_g_upn_lodochny, G_ichem, G_tagul, G_kchng,
        V_upsv_yu, V_upsv_s, V_cps, G_buying_oil, G_per, Q_vankor, V_upsv_yu_prev, V_upsv_s_prev, V_cps_prev, G_sikn_tagul, G_sikn_tng, V_cppn_1_0,V_gnps_0,
        VN_gnps_min, N
):
    V_suzun_slu = V_upn_suzun - V_suzun_vslu - V_suzun_tng
    G_suzun_slu = Q_suzun - Q_vslu - (V_suzun_slu - V_suzun_slu_prev) - K_delta_g_suzun
    G_suzun = G_suzun_slu + G_suzun_vslu + G_suzun_tng
    delta_G_suzun = Q_suzun - G_suzun_slu - G_suzun_vslu - (V_upn_suzun - V_upn_suzun_prev) + G_payaha
    V_lodochny = V_upn_lodochny - V_ichem
    G_upn_lodochny = Q_lodochny * K_otkachki - (V_upn_lodochny - V_upn_lodochny_prev) - K_delta_g_upn_lodochny/2 + Q_vo
    G_tagul_lodochny = G_tagul + G_upn_lodochny + G_kchng
    G_lodochny = G_upn_lodochny - G_ichem
    delta_G_upn_lodochny = round((Q_lodochny + Q_vo - G_lodochny_upsv_yu - G_lodochny - G_ichem - (V_upn_lodochny - V_upn_lodochny_prev))/100)*100
    V_cppn_1= V_upsv_yu + V_upsv_s + V_cps
    G_sikn_suzun = G_suzun + G_buying_oil - G_per
    G_sikn = Q_vankor + G_suzun - (V_upsv_yu - V_upsv_yu_prev) - (V_upsv_s - V_upsv_s_prev) - (V_cps - V_cps_prev) + G_lodochny_upsv_yu + G_buying_oil - G_per
    G_sikn_vankor = G_sikn - G_sikn_suzun - G_sikn_tagul - G_sikn_tng
    delta_G_sikn = round((Q_vankor + G_suzun + G_lodochny_upsv_yu - G_sikn - (V_cppn_1 - V_cppn_1_0) + G_buying_oil - G_per)/100)*100
    G_gpns_i = G_sikn + (V_gnps_0 - VN_gnps_min)/N
    return{
        "V_suzun_slu":V_suzun_slu,
        "G_suzun_slu":G_suzun_slu,
        "G_suzun":G_suzun,
        "delta_G_suzun":delta_G_suzun,
        "V_lodochny":V_lodochny,
        "G_upn_lodochny":G_upn_lodochny,
        "G_tagul_lodochny":G_tagul_lodochny,
        "G_lodochny":G_lodochny,
        "delta_G_upn_lodochny":delta_G_upn_lodochny,
        "V_cppn_1":V_cppn_1,
        "G_sikn_suzun":G_sikn_suzun,
        "G_sikn":G_sikn,
        "G_sikn_vankor":G_sikn_vankor,
        "delta_G_sikn":delta_G_sikn,
        "G_gpns_i":G_gpns_i,
    }
# ------------------------------------------------------------------
# Блок расчета планового баланса
# ------------------------------------------------------------------   
def rn_vankor_calc (
        F_vn_month, F_suzun_month, N, day, V_tstn_suzun_vslu_norm, F_tagul_lpu_month, F_tagul_tpu_month, F_skn_month, F_vo_month, F_kchng_month, 
        e_suzun, e_vo, e_kchng, e_tng, F_tng_month, G_suzun_vslu, F_suzun_vankor_month,  V_tstn_suzun_vslu_prev,
        F_bp_vn, F_bp_suzun, F_bp_suzun_vankor, F_bp_suzun_vslu, F_bp_tagul_lpu, F_bp_tagul_tpu, F_bp_skn, F_bp_vo, F_bp_tng, F_bp_kchng,
        bp_manual
):
    # Предварительный расчёт остаточных дней для каждой F_bp_* переменной
    bp_rdays = {}
    for _var, _manual in bp_manual.items():
        _rd = []
        for _d in range(N, 0, -1):
            if _d not in _manual:
                _rd.append(_d)
            if len(_rd) == 2:
                break
        bp_rdays[_var] = (set(_rd), sum(_manual.values()), N - len(_manual) - len(_rd), len(_rd))

# =========================================================
# 40. Ванкорнефть
    if not F_bp_vn:
        rset, msum, bcnt, rcnt = bp_rdays["F_bp_vn"]
        remaining = F_vn_month - msum
        auto_days = bcnt + rcnt
        base = round((remaining / auto_days) / 50) * 50 if auto_days > 0 else 0
        if day in rset:
            F_bp_vn = (remaining - base * bcnt) / rcnt if rcnt > 0 else 0
        else:
            F_bp_vn = base
    F_suzun = F_suzun_month - F_suzun_vankor_month
# =========================================================
# 41. Сузун (общий)
    if not F_bp_suzun:
        rset, msum, bcnt, rcnt = bp_rdays["F_bp_suzun"]
        remaining = F_suzun - msum
        auto_days = bcnt + rcnt
        base = round((remaining / auto_days) / 50) * 50 if auto_days > 0 else 0
        if day in rset:
            F_bp_suzun = (remaining - base * bcnt) / rcnt if rcnt > 0 else 0
        else:
            F_bp_suzun = base
# =========================================================
# 42. Сузун → Ванкор (через e)
    if not F_bp_suzun_vankor:
        if F_suzun_vankor_month < 20000:
            if e_suzun is None:
                raise CalculationValidationError(
                    f"Сузун → Ванкор: e не установлен"
                )
            elif not (e_suzun > 0):
                raise CalculationValidationError(
                    f"Сузун → Ванкор: e должно быть больше 0"
                )
            delivery_days = [d for d in range(1, N + 1) if d % e_suzun == 0]
            if delivery_days:
                manual_var = bp_manual.get("F_bp_suzun_vankor", {})
                msum_all = sum(manual_var.values())
                remaining = F_suzun_vankor_month - msum_all
                auto_delivery = [d for d in delivery_days if d not in manual_var]
                if day in auto_delivery:
                    auto_count = len(auto_delivery)
                    last_auto = auto_delivery[-1]
                    base = round((remaining / auto_count) / 50) * 50 if auto_count > 0 else 0
                    if day != last_auto:
                        F_bp_suzun_vankor = base
                    else:
                        F_bp_suzun_vankor = remaining - base * (auto_count - 1)
                else:
                    F_bp_suzun_vankor = 0
            else:
                F_bp_suzun_vankor = 0
        elif F_suzun_vankor_month >= 20000:
            rset, msum, bcnt, rcnt = bp_rdays["F_bp_suzun_vankor"]
            remaining = F_suzun_vankor_month - msum
            auto_days = bcnt + rcnt
            base = round((remaining / auto_days) / 50) * 50 if auto_days > 0 else 0
            if day in rset:
                F_bp_suzun_vankor = (remaining - base * bcnt) / rcnt if rcnt > 0 else 0
            else:
                F_bp_suzun_vankor = base
# =========================================================
# 43. Сузун → ВСЛУ
    V_tstn_suzun_vslu = V_tstn_suzun_vslu_prev + G_suzun_vslu - F_bp_suzun_vslu

    if V_tstn_suzun_vslu > V_tstn_suzun_vslu_norm + 1000:
        F_bp_suzun_vslu = 1000
    else:
        F_bp_suzun_vslu = 0
# =========================================================
# 44. Тагульское — ЛПУ
    if not F_bp_tagul_lpu:
        rset, msum, bcnt, rcnt = bp_rdays["F_bp_tagul_lpu"]
        remaining = F_tagul_lpu_month - msum
        auto_days = bcnt + rcnt
        base = round((remaining / auto_days) / 50) * 50 if auto_days > 0 else 0
        if day in rset:
            F_bp_tagul_lpu = (remaining - base * bcnt) / rcnt if rcnt > 0 else 0
        else:
            F_bp_tagul_lpu = base
# =========================================================
# 45. Тагульское — ТПУ
    if not F_bp_tagul_tpu:
        rset, msum, bcnt, rcnt = bp_rdays["F_bp_tagul_tpu"]
        remaining = F_tagul_tpu_month - msum
        auto_days = bcnt + rcnt
        base = round((remaining / auto_days) / 50) * 50 if auto_days > 0 else 0
        if day in rset:
            F_bp_tagul_tpu = (remaining - base * bcnt) / rcnt if rcnt > 0 else 0
        else:
            F_bp_tagul_tpu = base
# 46. Расчет суммарной сдачи ООО "Тагульское" через СИКН №1209
    F_bp_tagul = F_bp_tagul_lpu + F_bp_tagul_tpu
# =========================================================
# 47. СКН
    if not F_bp_skn:
        rset, msum, bcnt, rcnt = bp_rdays["F_bp_skn"]
        remaining = F_skn_month - msum
        auto_days = bcnt + rcnt
        base = round((remaining / auto_days) / 50) * 50 if auto_days > 0 else 0
        if day in rset:
            F_bp_skn = (remaining - base * bcnt) / rcnt if rcnt > 0 else 0
        else:
            F_bp_skn = base

# =========================================================
# 48. Восток Ойл (через e)   
    if not F_bp_vo:
        if F_vo_month < 20000:
            if e_vo is None:
                raise CalculationValidationError(
                    f"Восток Ойл: e не установлен"
                )
            elif not (e_vo > 0):
                raise CalculationValidationError(
                    f"Восток Ойл: e должно быть больше 0"
                )
            delivery_days = [d for d in range(1, N + 1) if d % e_vo == 0]
            if delivery_days:
                manual_var = bp_manual.get("F_bp_vo", {})
                msum_all = sum(manual_var.values())
                remaining = F_vo_month - msum_all
                auto_delivery = [d for d in delivery_days if d not in manual_var]
                if day in auto_delivery:
                    auto_count = len(auto_delivery)
                    last_auto = auto_delivery[-1]
                    base = round((remaining / auto_count) / 50) * 50 if auto_count > 0 else 0
                    if day != last_auto:
                        F_bp_vo = base
                    else:
                        F_bp_vo = remaining - base * (auto_count - 1)
                else:
                    F_bp_vo = 0
            else:
                F_bp_vo = 0
        else:
            rset, msum, bcnt, rcnt = bp_rdays["F_bp_vo"]
            remaining = F_vo_month - msum
            auto_days = bcnt + rcnt
            base = round((remaining / auto_days) / 50) * 50 if auto_days > 0 else 0
            if day in rset:
                F_bp_vo = (remaining - base * bcnt) / rcnt if rcnt > 0 else 0
            else:
                F_bp_vo = base
# =========================================================
# 49. Определение посуточной сдачи нефти АО "Таймырнефтегаз" через СИКН №1209
    if not F_bp_tng:
        if F_tng_month < 20000:
            if e_tng is None:
                raise CalculationValidationError(
                    f"Таймырнефтегаз: e не установлен"
                )
            elif not (e_tng > 0):
                raise CalculationValidationError(
                    f"Таймырнефтегаз: e должно быть больше 0"
                )
            delivery_days = [d for d in range(1, N + 1) if d % e_tng == 0]
            if delivery_days:
                manual_var = bp_manual.get("F_bp_tng", {})
                msum_all = sum(manual_var.values())
                remaining = F_tng_month - msum_all
                auto_delivery = [d for d in delivery_days if d not in manual_var]
                if day in auto_delivery:
                    auto_count = len(auto_delivery)
                    last_auto = auto_delivery[-1]
                    base = round((remaining / auto_count) / 50) * 50 if auto_count > 0 else 0
                    if day != last_auto:
                        F_bp_tng = base
                    else:
                        F_bp_tng = remaining - base * (auto_count - 1)
                else:
                    F_bp_tng = 0
            else:
                F_bp_tng = 0
        else:
            rset, msum, bcnt, rcnt = bp_rdays["F_bp_tng"]
            remaining = F_tng_month - msum
            auto_days = bcnt + rcnt
            base = round((remaining / auto_days) / 50) * 50 if auto_days > 0 else 0
            if day in rset:
                F_bp_tng = (remaining - base * bcnt) / rcnt if rcnt > 0 else 0
            else:
                F_bp_tng = base
# =========================================================
#  50.	Определение посуточной сдачи нефти ООО «КЧНГ» через СИКН № 1209, т/сут:
    if not F_bp_kchng:
        if F_kchng_month < 20000:
            if e_kchng is None:
                raise CalculationValidationError(
                    f"КЧНГ: e не установлен"
                )
            elif not (e_kchng > 0):
                raise CalculationValidationError(
                    f"КЧНГ: e должно быть больше 0"
                )
            delivery_days = [d for d in range(1, N + 1) if d % e_kchng == 0]
            if delivery_days:
                manual_var = bp_manual.get("F_bp_kchng", {})
                msum_all = sum(manual_var.values())
                remaining = F_kchng_month - msum_all
                auto_delivery = [d for d in delivery_days if d not in manual_var]
                if day in auto_delivery:
                    auto_count = len(auto_delivery)
                    last_auto = auto_delivery[-1]
                    base = round((remaining / auto_count) / 50) * 50 if auto_count > 0 else 0
                    if day != last_auto:
                        F_bp_kchng = base
                    else:
                        F_bp_kchng = remaining - base * (auto_count - 1)
                else:
                    F_bp_kchng = 0
            else:
                F_bp_kchng = 0
        else:
            rset, msum, bcnt, rcnt = bp_rdays["F_bp_kchng"]
            remaining = F_kchng_month - msum
            auto_days = bcnt + rcnt
            base = round((remaining / auto_days) / 50) * 50 if auto_days > 0 else 0
            if day in rset:
                F_bp_kchng = (remaining - base * bcnt) / rcnt if rcnt > 0 else 0
            else:
                F_bp_kchng = base
    F_bp = F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun
    return{
        "F_bp_vn":F_bp_vn,
        "F_bp_tagul_lpu":F_bp_tagul_lpu,
        "F_bp_tagul_tpu":F_bp_tagul_tpu,
        "F_bp_tagul":F_bp_tagul,
        "F_bp_suzun_vankor":F_bp_suzun_vankor,
        "F_bp_suzun_vslu":F_bp_suzun_vslu,
        "F_bp_skn":F_bp_skn,
        "F_bp_vo":F_bp_vo,
        "F_bp_tng":F_bp_tng,
        "F_bp_kchng":F_bp_kchng,
        "F_bp":F_bp,
        "F_bp_suzun":F_bp_suzun,
        "V_tstn_suzun_vslu":V_tstn_suzun_vslu,
    }
    # V_gnps = V_gnps_prev + G_sikn - G_gnps
# Расчет месячных значений
def availability_and_pumping_calc(G_gpns_i, N, V_gnps_prev, G_sikn, G_suzun_vslu,G_gnps):
    G_sikn_vslu = G_suzun_vslu
    G_gnps_month = G_gpns_i.sum()
    if not G_gnps:
        G_gnps = G_gnps_month/N
    V_gnps = V_gnps_prev + G_sikn - G_gnps


    return{
        "G_gnps_month":G_gnps_month,
        "G_gnps":G_gnps,
        "V_gnps":V_gnps,
        "G_sikn_vslu":G_sikn_vslu
    }
def month_calc (
        Q_vankor, Q_suzun, Q_vslu, Q_tng, Q_vo, Q_lodochny, G_suzun_vslu, G_sikn, G_sikn_tagul, G_sikn_suzun, G_sikn_tng, G_suzun_slu, G_sikn_vankor,
        G_skn, delta_G_sikn, delta_G_upn_lodochny, delta_G_tagul, G_suzun, G_sikn_vslu, G_lodochny, G_tagul_lodochny, delta_G_suzun, G_tagul, G_upn_lodochny_ichem,
        G_kchng, Q_kchng, G_per, V_ichem, G_upn_lodochny, F_bp_vn, F_bp_tagul_lpu, F_bp_tagul_tpu, F_bp_tagul, F_bp_suzun_vankor, F_bp_suzun_vslu,
        F_bp_skn, F_bp_vo, F_bp_tng, F_bp_kchng, F_bp, F_bp_suzun, day, N, G_ichem
):
    Q_vankor_month = Q_vankor.sum()
    Q_suzun_month = Q_suzun.sum()
    Q_vslu_month = Q_vslu.sum()
    Q_tng_month = Q_tng.sum()
    Q_vo_month = Q_vo.sum()
    Q_lodochny_month = Q_lodochny.sum()
    G_suzun_vslu_month = G_suzun_vslu.sum()
    G_sikn_vslu_month = G_sikn_vslu.sum()
    G_sikn_tng_month = G_sikn_tng.sum()
    G_ichem_month = G_ichem.sum()
    # G_suzun_slu приходит как числовой ряд (без словарей)
    G_suzun_slu_month = G_suzun_slu.sum()
    G_sikn_vankor_month = G_sikn_vankor.sum()
    G_sikn_month = G_sikn.sum()
    G_sikn_tagul_month = G_sikn_tagul.sum()
    G_sikn_suzun_month = G_sikn_suzun.sum()
    G_skn_month = G_skn.sum()
    delta_G_sikn_month = delta_G_sikn.sum()
    delta_G_upn_lodochny_month = delta_G_upn_lodochny.sum()
    delta_G_tagul_month = delta_G_tagul.sum()
    G_suzun_month = G_suzun.sum()
    G_lodochny_month = G_lodochny.sum()
    G_tagul_lodochny_month = G_tagul_lodochny.sum()
    delta_G_suzun_month = delta_G_suzun.sum()
    G_tagul_month = G_tagul.sum()
    G_upn_lodochny_ichem_month = G_upn_lodochny_ichem.sum()
    G_kchng_month = G_kchng.sum()
    Q_kchng_month = Q_kchng.sum()
    G_per_month = G_per.sum()
    V_ichem_month = V_ichem.sum()
    G_upn_lodochny_month = G_upn_lodochny.sum()
    F_bp_vn_month = F_bp_vn.sum()
    F_bp_tagul_lpu_month = F_bp_tagul_lpu.sum()
    F_bp_tagul_tpu_month = F_bp_tagul_tpu.sum()
    F_bp_tagul_month = F_bp_tagul.sum()
    F_bp_suzun_vankor_month = F_bp_suzun_vankor.sum()
    F_bp_suzun_vslu_month = F_bp_suzun_vslu.sum()
    F_bp_skn_month = F_bp_skn.sum()
    F_bp_vo_month = F_bp_vo.sum()
    F_bp_tng_month = F_bp_tng.sum()
    F_bp_kchng_month = F_bp_kchng.sum()
    F_bp_month = F_bp.sum()
    F_bp_suzun_month = F_bp_suzun.sum()
    F_bp_sr_month = F_bp_month/N

    _F_bp_day_flags = None
    if sum(F_bp[:10]) < F_bp_sr_month:
        _F_bp_day_flags = [
            {"value": float(F_bp[i]), "status": 2,
             "message": "Сдача за 1-10 сутки меньше среднесуточного значения за месяц"}
            for i in range(min(10, len(F_bp)))
        ]

    return {
        "_F_bp_day_flags": _F_bp_day_flags,
        "G_ichem_month":G_ichem_month,
        "F_bp_vn_month":F_bp_vn_month,
        "F_bp_tagul_lpu_month":F_bp_tagul_lpu_month,
        "F_bp_tagul_tpu_month":F_bp_tagul_tpu_month,
        "F_bp_tagul_month":F_bp_tagul_month,
        "F_bp_suzun_vankor_month":F_bp_suzun_vankor_month,
        "F_bp_suzun_vslu_month":F_bp_suzun_vslu_month,
        "F_bp_skn_month":F_bp_skn_month,
        "F_bp_vo_month":F_bp_vo_month,
        "F_bp_tng_month":F_bp_tng_month,
        "F_bp_kchng_month":F_bp_kchng_month,
        "F_bp_month":F_bp_month,
        "F_bp_suzun_month":F_bp_suzun_month,
        "F_bp_sr_month":F_bp_sr_month,
        "G_per_month":G_per_month,
        "V_ichem_month":V_ichem_month,
        "Q_vankor_month":Q_vankor_month,
        "Q_suzun_month":Q_suzun_month,
        "Q_vslu_month":Q_vslu_month,
        "Q_tng_month":Q_tng_month,
        "Q_vo_month":Q_vo_month,
        "Q_lodochny_month":Q_lodochny_month,
        "G_suzun_vslu_month":G_suzun_vslu_month,
        "G_sikn_vslu_month":G_sikn_vslu_month,
        "G_sikn_tng_month":G_sikn_tng_month,
        "G_suzun_slu_month":G_suzun_slu_month,
        "G_sikn_vankor_month":G_sikn_vankor_month,
        "G_sikn_month":G_sikn_month,
        "G_sikn_tagul_month":G_sikn_tagul_month,
        "G_sikn_suzun_month":G_sikn_suzun_month,
        "G_skn_month":G_skn_month,
        "delta_G_sikn_month":delta_G_sikn_month,
        "delta_G_upn_lodochny_month":delta_G_upn_lodochny_month,
        "delta_G_tagul_month":delta_G_tagul_month,
        "G_suzun_month":G_suzun_month,
        "G_lodochny_month":G_lodochny_month,
        "delta_G_suzun_month":delta_G_suzun_month,
        "G_tagul_lodochny_month":G_tagul_lodochny_month,
        "G_tagul_month":G_tagul_month,
        "G_upn_lodochny_ichem_month":G_upn_lodochny_ichem_month,
        "G_kchng_month":G_kchng_month,
        "Q_kchng_month":Q_kchng_month,
        "G_upn_lodochny_month":G_upn_lodochny_month,
    }
def auto_balance_volumes_calc(
        V_upn_suzun_prev, Start_autobalance, V_upn_suzun_0, VN_upn_suzun_min, V_upn_lodochny_0, VN_upn_lodochny_min,
        V_upsv_yu_0, VN_upsv_yu_min, V_upsv_s_0, VN_upsv_s_min,
        V_cps_0, VN_cps_min, V_upn_lodochny_prev, V_upsv_yu_prev, V_upsv_s_prev, V_cps_prev, N, V_upn_suzun,
        V_upn_lodochny, V_upsv_yu, V_upsv_s, V_cps,
):
    if Start_autobalance:
        V_upn_suzun = V_upn_suzun_prev - (V_upn_suzun_0 - VN_upn_suzun_min) / N
        V_upn_lodochny = V_upn_lodochny_prev - (V_upn_lodochny_0 - VN_upn_lodochny_min) / N
        V_upsv_yu = V_upsv_yu_prev - (V_upsv_yu_0 - VN_upsv_yu_min) / N
        V_upsv_s = V_upsv_s_prev - (V_upsv_s_0 - VN_upsv_s_min) / N
        V_cps = V_cps_prev - (V_cps_0 - VN_cps_min) / N
    return {
        "V_upn_suzun": V_upn_suzun, "V_upn_lodochny": V_upn_lodochny, "V_upsv_yu": V_upsv_yu, "V_upsv_s": V_upsv_s,
        "V_cps": V_cps,
    }


def rn_vankor_balance_calc (
        Start_autobalance, V_tstn_suzun_norm, VN_knps_min, V_tstn_suzun_prev, G_suzun_slu, K_suzun, F_bp_tagul_lpu, F_bp_tagul_tpu, F_bp_suzun_vankor,
        F_bp_suzun_vslu, F_bp_skn, F_bp_vo, F_bp_tng, F_bp_kchng, F_bp_vn, G_gnps, V_knps_prev, G_tagul, G_upn_lodochny, G_skn, G_kchng,
        V_nps_2, V_nps_2_prev, V_nps_1, V_nps_1_prev,  V_tstn_suzun_vankor_norm,V_tstn_suzun_vankor_prev,G_buying_oil,
        G_per, K_vankor,V_tstn_lodochny_prev, G_sikn_tagul, G_lodochny, K_lodochny, V_tstn_lodochny_norm, V_tstn_tagul_prev, 
        K_tagul, V_tstn_skn_prev, K_skn,V_tstn_vo_prev, G_ichem, K_ichem, V_tstn_tng_prev, G_suzun_tng, K_payaha, V_tstn_kchng_prev,
        V_tstn_tagul_norm,V_tstn_skn_norm, V_tstn_vo_norm, V_tstn_tng_norm, V_tstn_kchng_norm, V_gnps,V_tstn_rn_vn,
        V_tstn_suzun_vslu_prev, V_tstn_vn_norm, F_bp_suzun, F_bp, G_suzun_vslu
    ):

    # ------------------------------------------------------------------
    # Новый порядок (по твоему плану):
    # 1) Сначала корректируем все F_bp_* по своим ЦТН-диапазонам (без подгонки суммарного F_bp/КНПС).
    # 2) После этого подгоняем суммарный баланс через F_bp_vn (как "свободную ручку"),
    #    чтобы выполнить ограничения по КНПС и ЦТН ВН, не ломая ранее скорректированные ЦТН.
    # ------------------------------------------------------------------
    step = 50.0
    max_iter = 1000

    def _num(x, default=0.0):
        if isinstance(x, dict):
            x = x.get("value")
        try:
            return float(x)
        except (TypeError, ValueError):
            return default

    def _tune_bp(bp_init, calc_v, lower, upper):
        """Тюнинг F_bp_* шагом step до попадания calc_v(bp) в [lower, upper]."""
        bp = max(0.0, _num(bp_init))
        for _ in range(max_iter):
            v = calc_v(bp)
            if lower <= v <= upper:
                return bp, v, True
            if v > upper:
                bp += step
            else:
                bp = max(0.0, bp - step)
        return bp, calc_v(bp), False

    # флаги успешности корректировок (для статусов)
    ok_suzun = ok_suzun_vankor = ok_lodochny = ok_tagul = True
    ok_skn = ok_vo = ok_tng = ok_kchng = True
    ok_balance = True
    msg_suzun = msg_suzun_vankor = msg_lodochny = msg_tagul = None
    msg_skn = msg_vo = msg_tng = msg_kchng = None
    msg_balance = None

    # диапазон по КНПС
    knps_lower = _num(VN_knps_min) * 0.9
    knps_upper = _num(VN_knps_min) * 1.1

    # нормализуем числовые входы, которые точно участвуют в расчётах
    F_bp_suzun = _num(F_bp_suzun)
    F_bp_suzun_vankor = _num(F_bp_suzun_vankor)
    F_bp_suzun_vslu = _num(F_bp_suzun_vslu)
    F_bp_tagul_lpu = _num(F_bp_tagul_lpu)
    F_bp_tagul_tpu = _num(F_bp_tagul_tpu)
    F_bp_skn = _num(F_bp_skn)
    F_bp_vo = _num(F_bp_vo)
    F_bp_tng = _num(F_bp_tng)
    F_bp_kchng = _num(F_bp_kchng)
    F_bp_vn = _num(F_bp_vn)

    # ---- ЭТАП 1: локальные корректировки F_bp_* (кроме суммарного баланса) ----
    if Start_autobalance:
        # Сузун (BY)
        suzun_lower = _num(V_tstn_suzun_norm) * 0.9
        suzun_upper = _num(V_tstn_suzun_norm) * 1.1

        def _v_suzun(bp):
            return _num(V_tstn_suzun_prev) - bp + _num(G_suzun_slu) - bp * (_num(K_suzun) / 100.0)

        F_bp_suzun, V_tstn_suzun, ok_suzun = _tune_bp(F_bp_suzun, _v_suzun, suzun_lower, suzun_upper)
        if not ok_suzun:
            msg_suzun = (
                f"Не удалось скорректировать F_bp_suzun за {max_iter} итераций. "
                f"V_tstn_suzun={V_tstn_suzun:.2f}, диапазон [{suzun_lower:.2f}; {suzun_upper:.2f}]"
            )

        # Сузун → Ванкор (BZ) — тюним только если план большой (как и было)
        def _v_suzun_vankor(bp):
            return (
                _num(V_tstn_suzun_vankor_prev)
                - bp
                + (_num(G_buying_oil) - _num(G_per))
                - bp * (_num(K_vankor) / 100.0)
            )

        if F_bp_suzun_vankor >= 20000:
            suzun_vankor_lower = _num(V_tstn_suzun_vankor_norm) * 0.9
            suzun_vankor_upper = _num(V_tstn_suzun_vankor_norm) * 1.1
            F_bp_suzun_vankor, V_tstn_suzun_vankor, ok_suzun_vankor = _tune_bp(
                F_bp_suzun_vankor, _v_suzun_vankor, suzun_vankor_lower, suzun_vankor_upper
            )
            if not ok_suzun_vankor:
                msg_suzun_vankor = (
                    f"Не удалось скорректировать F_bp_suzun_vankor за {max_iter} итераций. "
                    f"V_tstn_suzun_vankor={V_tstn_suzun_vankor:.2f}, диапазон [{suzun_vankor_lower:.2f}; {suzun_vankor_upper:.2f}]"
                )
        else:
            V_tstn_suzun_vankor = _v_suzun_vankor(F_bp_suzun_vankor)
            ok_suzun_vankor = True
            msg_suzun_vankor = None

        # Сузун → ВСЛУ (норма не передаётся — считаем по факту)
        V_tstn_suzun_vslu = (
            _num(V_tstn_suzun_vslu_prev)
            - F_bp_suzun_vslu
            + _num(G_suzun_vslu)
            - F_bp_suzun_vslu * (_num(K_suzun) / 100.0)
        )

        # Лодочное (через F_bp_tagul_lpu)
        lodochny_lower = _num(V_tstn_lodochny_norm) * 0.9
        lodochny_upper = _num(V_tstn_lodochny_norm) * 1.1

        def _v_lodochny(bp):
            return (
                _num(V_tstn_lodochny_prev)
                + _num(G_sikn_tagul)
                + _num(G_lodochny)
                - bp
                - bp * (_num(K_lodochny) / 100.0)
            )

        F_bp_tagul_lpu, V_tstn_lodochny, ok_lodochny = _tune_bp(
            F_bp_tagul_lpu, _v_lodochny, lodochny_lower, lodochny_upper
        )
        if not ok_lodochny:
            msg_lodochny = (
                f"Не удалось скорректировать F_bp_tagul_lpu за {max_iter} итераций. "
                f"V_tstn_lodochny={V_tstn_lodochny:.2f}, диапазон [{lodochny_lower:.2f}; {lodochny_upper:.2f}]"
            )

        # Тагул (через F_bp_tagul_tpu)
        tagul_lower = _num(V_tstn_tagul_norm) * 0.9
        tagul_upper = _num(V_tstn_tagul_norm) * 1.1

        def _v_tagul(bp):
            return _num(V_tstn_tagul_prev) + _num(G_tagul) - bp - bp * (_num(K_tagul) / 100.0)

        F_bp_tagul_tpu, V_tstn_tagul, ok_tagul = _tune_bp(F_bp_tagul_tpu, _v_tagul, tagul_lower, tagul_upper)
        if not ok_tagul:
            msg_tagul = (
                f"Не удалось скорректировать F_bp_tagul_tpu за {max_iter} итераций. "
                f"V_tstn_tagul={V_tstn_tagul:.2f}, диапазон [{tagul_lower:.2f}; {tagul_upper:.2f}]"
            )
        V_tstn_tagul_obsh = V_tstn_tagul + V_tstn_lodochny

        # СКН
        skn_lower = _num(V_tstn_skn_norm) * 0.9
        skn_upper = _num(V_tstn_skn_norm) * 1.1

        def _v_skn(bp):
            return _num(V_tstn_skn_prev) - bp + _num(G_skn) - bp * (_num(K_skn) / 100.0)

        F_bp_skn, V_tstn_skn, ok_skn = _tune_bp(F_bp_skn, _v_skn, skn_lower, skn_upper)
        if not ok_skn:
            msg_skn = (
                f"Не удалось скорректировать F_bp_skn за {max_iter} итераций. "
                f"V_tstn_skn={V_tstn_skn:.2f}, диапазон [{skn_lower:.2f}; {skn_upper:.2f}]"
            )

        # ВО
        vo_lower = _num(V_tstn_vo_norm) * 0.9
        vo_upper = _num(V_tstn_vo_norm) * 1.1

        def _v_vo(bp):
            return _num(V_tstn_vo_prev) + _num(G_ichem) - bp - bp * (_num(K_ichem) / 100.0)

        F_bp_vo, V_tstn_vo, ok_vo = _tune_bp(F_bp_vo, _v_vo, vo_lower, vo_upper)
        if not ok_vo:
            msg_vo = (
                f"Не удалось скорректировать F_bp_vo за {max_iter} итераций. "
                f"V_tstn_vo={V_tstn_vo:.2f}, диапазон [{vo_lower:.2f}; {vo_upper:.2f}]"
            )

        # ТНГ
        tng_lower = _num(V_tstn_tng_norm) * 0.9
        tng_upper = _num(V_tstn_tng_norm) * 1.1

        def _v_tng(bp):
            return _num(V_tstn_tng_prev) + _num(G_suzun_tng) - bp - bp * (_num(K_payaha) / 100.0)

        F_bp_tng, V_tstn_tng, ok_tng = _tune_bp(F_bp_tng, _v_tng, tng_lower, tng_upper)
        if not ok_tng:
            msg_tng = (
                f"Не удалось скорректировать F_bp_tng за {max_iter} итераций. "
                f"V_tstn_tng={V_tstn_tng:.2f}, диапазон [{tng_lower:.2f}; {tng_upper:.2f}]"
            )

        # КЧНГ
        kchng_lower = _num(V_tstn_kchng_norm) * 0.9
        kchng_upper = _num(V_tstn_kchng_norm) * 1.1

        def _v_kchng(bp):
            return _num(V_tstn_kchng_prev) + _num(G_kchng) - bp - bp * (_num(K_tagul) / 100.0)

        F_bp_kchng, V_tstn_kchng, ok_kchng = _tune_bp(F_bp_kchng, _v_kchng, kchng_lower, kchng_upper)
        if not ok_kchng:
            msg_kchng = (
                f"Не удалось скорректировать F_bp_kchng за {max_iter} итераций. "
                f"V_tstn_kchng={V_tstn_kchng:.2f}, диапазон [{kchng_lower:.2f}; {kchng_upper:.2f}]"
            )

        # ---- ЭТАП 2: подгонка суммарного баланса через F_bp_vn ----
        vn_lower = _num(V_tstn_vn_norm) * 0.9
        vn_upper = _num(V_tstn_vn_norm) * 1.1

        def _calc_totals(bp_vn):
            bp_total = (
                bp_vn
                + F_bp_tagul_lpu + F_bp_tagul_tpu
                + F_bp_suzun_vankor + F_bp_suzun_vslu
                + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng
                + F_bp_suzun
            )
            v_knps = (
                _num(G_gnps)
                - bp_total
                + _num(V_knps_prev)
                + _num(G_tagul)
                + _num(G_upn_lodochny)
                + _num(G_skn)
                + _num(G_kchng)
                - (_num(V_nps_2) - _num(V_nps_2_prev))
                - (_num(V_nps_1) - _num(V_nps_1_prev))
            )
            v_tstn = _num(V_gnps) + _num(V_nps_1) + _num(V_nps_2) + v_knps
            v_vn = (
                v_tstn
                - _num(V_tstn_rn_vn)
                - V_tstn_suzun
                - V_tstn_tagul_obsh
                - V_tstn_suzun_vankor
                - V_tstn_suzun_vslu
                - V_tstn_skn
                - V_tstn_vo
                - V_tstn_tng
                - V_tstn_kchng
            )
            return bp_total, v_knps, v_vn

        iter_count = 0
        while True:
            iter_count += 1
            F_bp, V_knps, V_tstn_vn = _calc_totals(F_bp_vn)
            knps_ok = knps_lower <= V_knps <= knps_upper
            vn_ok = vn_lower <= V_tstn_vn <= vn_upper
            if knps_ok and vn_ok:
                break

            vn_dir = 1 if V_tstn_vn > vn_upper else (-1 if V_tstn_vn < vn_lower else 0)
            knps_dir = 1 if V_knps > knps_upper else (-1 if V_knps < knps_lower else 0)

            if vn_dir == 0:
                direction = knps_dir
            elif knps_dir == 0 or vn_dir == knps_dir:
                direction = vn_dir
            else:
                # при конфликте приоритет за ЦТН ВН
                direction = vn_dir

            if direction > 0:
                F_bp_vn += step
            elif direction < 0:
                F_bp_vn = max(0.0, F_bp_vn - step)
            else:
                break

            if iter_count > max_iter:
                # не удалось скорректировать — выходим с текущими значениями
                break

        # финальная проверка: удалось ли попасть в коридоры
        F_bp, V_knps, V_tstn_vn = _calc_totals(F_bp_vn)
        ok_balance = (knps_lower <= V_knps <= knps_upper) and (vn_lower <= V_tstn_vn <= vn_upper)
        if not ok_balance:
            msg_balance = (
                f"Не удалось скорректировать баланс за {max_iter} итераций. "
                f"V_knps={V_knps:.2f} (целевой [{knps_lower:.2f}; {knps_upper:.2f}]), "
                f"V_tstn_vn={V_tstn_vn:.2f} (целевой [{vn_lower:.2f}; {vn_upper:.2f}])"
            )

    # итоговые значения (в т.ч. когда Start_autobalance=False)
    F_bp = (
        F_bp_vn
        + F_bp_tagul_lpu + F_bp_tagul_tpu
        + F_bp_suzun_vankor + F_bp_suzun_vslu
        + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng
        + F_bp_suzun
    )

    def _wrap(value, ok, message=None):
        return {"value": value, "status": 1 if ok else 3, "message": (None if ok else message)}

    # Числовые значения (для сборки сумм)
    _F_suzun = F_bp_suzun
    _F_suzun_vankor = F_bp_suzun_vankor
    _F_suzun_vslu = F_bp_suzun_vslu
    _F_tagul_lpu = F_bp_tagul_lpu
    _F_tagul_tpu = F_bp_tagul_tpu
    _F_tagul = _F_tagul_lpu + _F_tagul_tpu
    _F_skn = F_bp_skn
    _F_vo = F_bp_vo
    _F_tng = F_bp_tng
    _F_kchng = F_bp_kchng
    _F_vn = F_bp_vn
    _F = F_bp

    # Статусы: 1 — норм, 3 — не удалось скорректировать
    if not Start_autobalance:
        ok_suzun = ok_suzun_vankor = ok_lodochny = ok_tagul = True
        ok_skn = ok_vo = ok_tng = ok_kchng = True
        ok_balance = True
        msg_suzun = msg_suzun_vankor = msg_lodochny = msg_tagul = None
        msg_skn = msg_vo = msg_tng = msg_kchng = None
        msg_balance = None

    F_suzun = _wrap(_F_suzun, ok_suzun, msg_suzun)
    F_suzun_vankor = _wrap(_F_suzun_vankor, ok_suzun_vankor, msg_suzun_vankor)
    # F_suzun_vslu не корректируем (берём как есть)
    F_suzun_vslu = _wrap(_F_suzun_vslu, True, None)

    F_tagul_lpu = _wrap(_F_tagul_lpu, ok_lodochny, msg_lodochny)
    F_tagul_tpu = _wrap(_F_tagul_tpu, ok_tagul, msg_tagul)
    F_tagul = _wrap(_F_tagul, (ok_lodochny and ok_tagul), (msg_lodochny or msg_tagul))

    F_skn = _wrap(_F_skn, ok_skn, msg_skn)
    F_vo = _wrap(_F_vo, ok_vo, msg_vo)
    F_tng = _wrap(_F_tng, ok_tng, msg_tng)
    F_kchng = _wrap(_F_kchng, ok_kchng, msg_kchng)

    F_vn = _wrap(_F_vn, ok_balance, msg_balance)
    F = _wrap(_F, ok_balance, msg_balance)

    return{
        # Фактические F_* в формате {value,status,message} — для UI/контроля
        "F_suzun_vankor": F_suzun_vankor,
        "F_tagul_lpu": F_tagul_lpu,
        "F_tagul_tpu": F_tagul_tpu,
        "F_vn": F_vn,
        "F": F,
        "F_skn": F_skn,
        "F_vo": F_vo,
        "F_tng": F_tng,
        "F_kchng": F_kchng,
        "F_suzun_vslu": F_suzun_vslu,
        "F_tagul": F_tagul,
        "F_suzun":F_suzun,
    }
    
def bp_month_calc (F_suzun_vankor, F_tagul_lpu, F_tagul_tpu, F_vn, F, F_skn, F_vo, F_tng, F_kchng, F_suzun_vslu, F_tagul, F_suzun):
    F_suzun_vankor_sum = F_suzun_vankor.sum()
    F_tagul_lpu_sum = F_tagul_lpu.sum()
    F_tagul_tpu_sum = F_tagul_tpu.sum()
    F_vn_sum = F_vn.sum()
    F_sum = F.sum()
    F_skn_sum = F_skn.sum()
    F_vo_sum = F_vo.sum()
    F_tng_sum = F_tng.sum()
    F_kchng_sum = F_kchng.sum()
    F_suzun_vslu_sum = F_suzun_vslu.sum()
    F_tagul_sum = F_tagul.sum()
    F_suzun_sum = F_suzun.sum()
    return{
        "F_suzun_sum":F_suzun_sum,
        "F_suzun_vankor_sum":F_suzun_vankor_sum,
        "F_tagul_sum":F_tagul_sum,
        "F_tagul_lpu_sum":F_tagul_lpu_sum,
        "F_tagul_tpu_sum":F_tagul_tpu_sum,
        "F_vn_sum":F_vn_sum,
        "F_sum":F_sum,
        "F_skn_sum":F_skn_sum,
        "F_vo_sum":F_vo_sum,
        "F_tng_sum":F_tng_sum,
        "F_kchng_sum":F_kchng_sum,
        "F_suzun_vslu_sum":F_suzun_vslu_sum,
    }
def availability_oil_calc (
        V_tstn_suzun_vslu_prev, F_suzun_vslu, G_suzun_vslu, K_suzun, V_tstn_tagul_prev,  G_tagul, F_tagul_tpu, K_tagul, V_tstn_lodochny_prev,
        G_sikn_tagul, G_lodochny, F_tagul_lpu, K_lodochny, V_tstn_suzun_prev, F_suzun, G_suzun_slu, V_tstn_suzun_vankor_prev, F_suzun_vankor,
        G_buying_oil, G_per, K_vankor, V_tstn_skn_prev, F_skn, G_skn, K_skn, V_tstn_vo_prev, G_ichem, F_vo, K_ichem, K_payaha, F_tng,
        V_tstn_tng_prev, G_suzun_tng,  V_tstn_kchng_prev, G_kchng, F_kchng, G_upn_lodochny, V_knps_prev, F, G_gnps, V_nps_2, V_nps_1,V_nps_2_prev,
        V_nps_1_prev, V_gnps, V_tstn_rn_vn
):
    V_tstn_suzun_vslu = V_tstn_suzun_vslu_prev - F_suzun_vslu + G_suzun_vslu - F_suzun_vslu * (K_suzun / 100)
    V_tstn_tagul = V_tstn_tagul_prev + G_tagul - F_tagul_tpu - F_tagul_tpu * (K_tagul / 100)
    V_tstn_lodochny = V_tstn_lodochny_prev + G_sikn_tagul + G_lodochny - F_tagul_lpu - F_tagul_lpu * (K_lodochny / 100)
    V_tstn_tagul_obsh = V_tstn_tagul + V_tstn_lodochny 
    V_tstn_suzun = (V_tstn_suzun_prev - F_suzun + G_suzun_slu - F_suzun * (K_suzun / 100))
    V_tstn_suzun_vankor = V_tstn_suzun_vankor_prev - F_suzun_vankor + (G_buying_oil - G_per) - F_suzun_vankor * (K_vankor/100)
    V_tstn_skn = V_tstn_skn_prev - F_skn + G_skn - F_skn * (K_skn/100)
    V_tstn_vo = V_tstn_vo_prev + G_ichem - F_vo - F_vo * (K_ichem/100)
    V_tstn_tng = V_tstn_tng_prev + G_suzun_tng - F_tng - F_tng * (K_payaha/100)
    V_tstn_kchng = V_tstn_kchng_prev + G_kchng - F_kchng - F_kchng * (K_tagul/100)
    V_knps = (
                G_gnps - F + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng
                - (V_nps_2 - V_nps_2_prev) - (V_nps_1 - V_nps_1_prev)
            )
    V_tstn = V_gnps + V_nps_1 + V_nps_2 + V_knps
    V_tstn_vn = (
                V_tstn - V_tstn_rn_vn - V_tstn_suzun - V_tstn_tagul_obsh - V_tstn_suzun_vankor
                - V_tstn_suzun_vslu - V_tstn_skn - V_tstn_vo - V_tstn_tng - V_tstn_kchng
            )
    return{
        "V_tstn_suzun_vslu":V_tstn_suzun_vslu,
        "V_tstn_tagul":V_tstn_tagul,
        "V_tstn_lodochny":V_tstn_lodochny,
        "V_tstn_tagul_obsh":V_tstn_tagul_obsh,
        "V_tstn_suzun":V_tstn_suzun,
        "V_tstn_suzun_vankor":V_tstn_suzun_vankor,
        "V_tstn_skn":V_tstn_skn,
        "V_tstn_vo":V_tstn_vo,
        "V_tstn_tng":V_tstn_tng,
        "V_tstn_kchng":V_tstn_kchng,
        "V_knps":V_knps,
        "V_tstn":V_tstn,
        "V_tstn_vn":V_tstn_vn

}


def rn_vankor_check_calc(
        VA_upsv_yu_min, V_upsv_yu, VA_upsv_yu_max, V_upsv_yu_prev, delta_V_upsv_yu_max, delta_VO_upsv_yu_max,VA_upsv_s_min, V_upsv_s,
        VA_upsv_s_max, V_upsv_s_prev, delta_V_upsv_s_max, delta_VO_upsv_s_max, VA_cps_min, V_cps, VA_cps_max,V_cps_prev, delta_V_cps_max,
        delta_VO_cps_max, VA_upn_suzun_min, V_upn_suzun, VA_upn_suzun_max, V_upn_suzun_prev, delta_V_upn_suzun_max, delta_VO_upn_suzun_max,
        VA_upn_lodochny_min, V_upn_lodochny, VA_upn_lodochny_max, V_upn_lodochny_prev, delta_V_upn_lodochny_max, delta_VO_upn_lodochny_max,
        VA_tagul_min, V_tagul_tr, VA_tagul_max, VA_gnps_min, V_gnps, VA_gnps_max, V_gnps_prev, delta_V_gnps_max, delta_VO_gnps_max,
        VA_nps_1_min, V_nps_1, VA_nps_1_max, V_nps_1_prev, delta_V_nps_1_max, delta_VO_nps_1_max, VA_nps_2_min, V_nps_2, VA_nps_2_max,
        V_nps_2_prev, delta_V_nps_2_max, delta_VO_nps_2_max, VN_knps_min, V_knps, VA_knps_max, V_knps_prev, delta_V_knps_max,
        delta_VO_knps_max, V_ichem_min, V_ichem, V_ichem_max, V_lodochny_cps_upsv_yu, G_sikn_tagul, G_sikn_tagul_is_manual, V_tstn_vn_min, V_tstn_vn, V_tstn_vn_max,
        V_tstn_suzun_min, V_tstn_suzun, V_tstn_suzun_max, V_tstn_suzun_vankor_min, V_tstn_suzun_vankor, V_tstn_suzun_vankor_max, V_tstn_suzun_vslu_min,
        V_tstn_suzun_vslu, V_tstn_suzun_vslu_max, V_tstn_tagul_obsh_min, V_tstn_tagul_obsh, V_tstn_tagul_obsh_max, V_tstn_lodochny_min,
        V_tstn_lodochny, V_tstn_lodochny_max, V_tstn_tagul_min, V_tstn_tagul, V_tstn_tagul_max, V_tstn_skn_min, V_tstn_skn, V_tstn_skn_max,
        V_tstn_vo_min, V_tstn_vo, V_tstn_vo_max, V_tstn_tng_min, V_tstn_tng, V_tstn_tng_max, V_tstn_kchng_min, V_tstn_kchng, V_tstn_kchng_max,
        G_gnps, p_gnps, Q_gnps_min1, Q_gnps_max2, Q_gnps_max1, G_tagul_lodochny, p_nps_1_2, Q_nps_1_2_min1, Q_nps_1_2_max2, Q_nps_1_2_max1,
        p_knps, Q_knps_min1, Q_knps_max2, Q_knps_max1, F
):
    # --- 83. Проверка выполнения условий по наличию нефти на УПСВ-Юг
    V_upsv_yu = {"value": (V_upsv_yu.get("value") if isinstance(V_upsv_yu, dict) else V_upsv_yu), "status": 0, "message": ""}
    if VA_upsv_yu_min <= V_upsv_yu["value"] <= VA_upsv_yu_max:
        V_upsv_yu.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти на УПСВ-Юг выполнена"})
    else:
        if V_upsv_yu["value"] < VA_upsv_yu_min:
            msg = "Наличие нефти в РП УПСВ-Юг ниже минимального допустимого значения, необходимо уменьшить откачку нефти на СИКН-1208 путем увеличения (ручным вводом) наличия нефти в РП УПСВ-Юг (столбец F) до нужного значения"
            V_upsv_yu.update({"status": 3, "message": msg})
        elif V_upsv_yu["value"] > VA_upsv_yu_max:
            msg = "Наличие нефти в РП УПСВ-Юг выше максимально допустимого значения, необходимо увеличить откачку нефти на СИКН-1208 путем уменьшения (ручным вводом) наличия нефти в РП УПСВ-Юг (столбец F) до нужного значения"
            V_upsv_yu.update({"status": 3, "message": msg})
    delta_upsv_yu = V_upsv_yu["value"] - V_upsv_yu_prev
    if delta_upsv_yu >= 0:
        if abs(delta_upsv_yu) > delta_V_upsv_yu_max:
            msg = "Скорость наполнения РП УПСВ-Юг больше допустимой величины, необходимо увеличить откачку нефти на СИКН-1208 путем уменьшения (ручным вводом) наличия нефти в РП УПСВ-Юг (столбец F) до нужного значения"
            V_upsv_yu.update({"status": 3, "message": msg})
    else:
        if abs(delta_upsv_yu) > delta_VO_upsv_yu_max:
            msg = "Скорость опорожнения РП УПСВ-Юг больше допустимой величины, необходимо уменьшить откачку нефти на СИКН-1208 путем увеличения (ручным вводом) наличия нефти в РП УПСВ-Юг (столбец F) до нужного значения"
            V_upsv_yu.update({"status": 3, "message": msg})

    # --- 84. Проверка выполнения условий по наличию нефти на УПСВ-Север
    V_upsv_s = {"value": (V_upsv_s.get("value") if isinstance(V_upsv_s, dict) else V_upsv_s), "status": 0, "message": ""}
    if VA_upsv_s_min <= V_upsv_s["value"] <= VA_upsv_s_max:
        V_upsv_s.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти на УПСВ-Север выполнена"})
    else:
        if V_upsv_s["value"] < VA_upsv_s_min:
            msg = "Наличие нефти в РП УПСВ-Север ниже минимального допустимого значения, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП УПСВ-Север (столбец G) до нужного значения"
            V_upsv_s.update({"status": 3, "message": msg})
        elif V_upsv_s["value"] > VA_upsv_s_max:
            msg = "Наличие нефти в РП УПСВ-Север выше максимально допустимого значения, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП УПСВ-Север (столбец G) до нужного значения"
            V_upsv_s.update({"status": 3, "message": msg})
    delta_upsv_s = V_upsv_s["value"] - V_upsv_s_prev
    if delta_upsv_s >= 0:
        if abs(delta_upsv_s) > delta_V_upsv_s_max:
            msg = "Скорость наполнения РП УПСВ Север больше допустимой величины, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП УПСВ Север (столбец G) до нужного значения"
            V_upsv_s.update({"status": 3, "message": msg})
        else:
            V_upsv_s.update({"status": 1,
                                 "message": "Проверка выполнения условий по скорости наполнения РП на УПСВ-Север выполнена"})
    else:
        if abs(delta_upsv_s) > delta_VO_upsv_s_max:
            msg = "Скорость опорожнения РП УПСВ Север больше допустимой величины, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП УПСВ Север (столбец G) до нужного значения"
            V_upsv_s.update({"status": 3, "message": msg})
        else:
            V_upsv_s.update({"status": 1,
                                 "message": "Проверка выполнения условий по скорости наполнения РП на УПСВ-Север выполнена"})

    # --- 85. Проверка выполнения условий по наличию нефти на ЦПС
    V_cps = {"value": (V_cps.get("value") if isinstance(V_cps, dict) else V_cps), "status": 0, "message": ""}
    if VA_cps_min <= V_cps["value"] <= VA_cps_max:
        V_cps.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на ЦПС выполнена"})
    else:
        if V_cps["value"] < VA_cps_min:
            msg = "Наличие нефти в РП ЦПС ниже минимального допустимого значения, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП ЦПС (столбец H) до нужного значения"
            V_cps.update({"status": 3, "message": msg})
        elif V_cps["value"] > VA_cps_max:
            msg = "Наличие нефти в РП ЦПС выше максимально допустимого значения, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП ЦПС (столбец H) до нужного значения"
            V_cps.update({"status": 3, "message": msg})
    delta_cps = V_cps["value"] - V_cps_prev
    if delta_cps >= 0:
        if abs(delta_cps) > delta_V_cps_max:
            msg = "Скорость наполнения РП ЦПС больше допустимой величины, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП ЦПС (столбец H) до нужного значения"
            V_cps.update({"status": 3, "message": msg})
    else:
        if abs(delta_cps) > delta_VO_cps_max:
            msg = "Скорость опорожнения РП ЦПС больше допустимой величины, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП ЦПС (столбец H) до нужного значения"
            V_cps.update({"status": 3, "message": msg})

    # --- 86. Проверка выполнения условий по наличию нефти на УПН Сузун
    V_upn_suzun = {"value": (V_upn_suzun.get("value") if isinstance(V_upn_suzun, dict) else V_upn_suzun), "status": 0, "message": ""}
    if VA_upn_suzun_min <= V_upn_suzun["value"] <= VA_upn_suzun_max:
        V_upn_suzun.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти на УПН Сузун выполнена"})
    else:
        if V_upn_suzun["value"] < VA_upn_suzun_min:
            msg = "Наличие нефти в РП УПН Сузун ниже минимального допустимого значения, необходимо уменьшить откачку нефти на СИКН-1208 путем увеличения (ручным вводом) наличия нефти в РП УПН Сузун (столбец V) до нужного значения"
            V_upn_suzun.update({"status": 2, "message": msg})
        elif V_upn_suzun["value"] > VA_upn_suzun_max:
            msg = "Наличие нефти в РП УПН Сузун выше максимально допустимого значения, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП УПН Сузун (столбец V) до нужного значения"
            V_upn_suzun.update({"status": 3, "message": msg})
    delta_upn_suzun = V_upn_suzun["value"] - V_upn_suzun_prev
    if delta_upn_suzun >= 0:
        if abs(delta_upn_suzun) > delta_V_upn_suzun_max:
            msg = "Скорость наполнения РП УПН Сузун больше допустимой величины, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП УПН Сузун (столбец V) до нужного значения"
            V_upn_suzun.update({"status": 3, "message": msg})
    else:
        if abs(delta_upn_suzun) > delta_VO_upn_suzun_max:
            msg = "Скорость опорожнения РП УПН Сузун больше допустимой величины, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП УПН Сузун (столбец V) до нужного значения"
            V_upn_suzun.update({"status": 3, "message": msg})

    # --- 87. Проверка выполнения условий по наличию нефти на УПН Лодочное
    V_upn_lodochny = {"value": (V_upn_lodochny.get("value") if isinstance(V_upn_lodochny, dict) else V_upn_lodochny), "status": 0, "message": ""}
    if VA_upn_lodochny_min <= V_upn_lodochny["value"] <= VA_upn_lodochny_max:
        V_upn_lodochny.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти на УПН Лодочное выполнена"})
    else:
        if V_upn_lodochny["value"] < VA_upn_lodochny_min:
            msg = "Наличие нефти в РП УПН Лодочное ниже минимально допустимого значения, необходимо уменьшить откачку нефти на СИКН-1208 путем увеличения (ручным вводом) наличия нефти в РП УПН Лодочное (столбец AR) до нужного значения"
            V_upn_lodochny.update({"status": 3, "message": msg})
        elif V_upn_lodochny["value"] > VA_upn_lodochny_max:
            msg = "Наличие нефти в РП УПН Лодочное выше максимально допустимого значения, необходимо увеличить откачку нефти на СИКН-1208 путем уменьшения (ручным вводом) наличия нефти в РП УПН Лодочное (столбец AR) до нужного значения"
            V_upn_lodochny.update({"status": 3, "message": msg})
    delta_upn_lodochny = V_upn_lodochny["value"] - V_upn_lodochny_prev
    if delta_upn_lodochny >= 0:
        if abs(delta_upn_lodochny) > delta_V_upn_lodochny_max:
            msg = "Скорость наполнения РП УПН Лодочное больше допустимой величины, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП УПН Лодочное (столбец AR) до нужного значения"
            V_upn_lodochny.update({"status": 3, "message": msg})
    else:
        if abs(delta_upn_lodochny) > delta_VO_upn_lodochny_max:
            msg = "Скорость опорожнения РП УПН Лодочное больше допустимой величины, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП УПН Лодочное (столбец AR) до нужного значения"
            V_upn_lodochny.update({"status": 3, "message": msg})

    # --- 88. Проверка выполнения условий по наличию нефти на Тагульском месторождении
    V_tagul_tr = {"value": (V_tagul_tr.get("value") if isinstance(V_tagul_tr, dict) else V_tagul_tr), "status": 0, "message": ""}
    if VA_tagul_min <= V_tagul_tr["value"] <= VA_tagul_max:
        V_tagul_tr.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти на Тагульском месторождении"})
    else:
        if V_tagul_tr["value"] < VA_tagul_min:
            msg = "Наличие нефти в трубопроводах и аппаратах ООО «Тагульское» ниже минимально допустимого значения, необходимо уменьшить откачку нефти в магистральный нефтепровод путем увеличения (ручным вводом) наличия нефти в трубопроводах и аппаратах ООО «Тагульское» (столбец AL) до нужного значения"
            V_tagul_tr.update({"status": 3, "message": msg})
        elif V_tagul_tr["value"] > VA_tagul_max:
            msg = "Наличие нефти в трубопроводах и аппаратах ООО «Тагульское» выше максимально допустимого значения, необходимо увеличить откачку нефти в магистральный нефтепровод путем уменьшения (ручным вводом) наличия нефти в трубопроводах и аппаратах ООО «Тагульское» (столбец AL) до нужного значения"
            V_tagul_tr.update({"status": 3, "message": msg})
    # --- 89. Проверка выполнения условий по наличию нефти на ГНПС
    V_gnps = {"value": (V_gnps.get("value") if isinstance(V_gnps, dict) else V_gnps), "status": 0, "message": ""}
    if VA_gnps_min <= V_gnps["value"] <= VA_gnps_max:
        V_gnps.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на ГНПС выполнена"})
    else:
        if V_gnps["value"] < VA_gnps_min:
            msg = "Наличие нефти в РП ГНПС ниже минимального допустимого значения, необходимо либо уменьшить (путем ручного ввода нужного значения) откачку нефти с ГНПС (столбец BE), либо увеличить поступление нефти через СИКН-1208 [путем уменьшения ручным вводом наличия нефти в РП УПСВ-Ю (столбец F), УПСВ-С (столбец G), ЦПС (столбец H) до нужных показателей]"
            V_gnps.update({"status": 2, "message": msg})
        elif V_gnps["value"] > VA_gnps_max:
            msg = "Наличие нефти в РП ГНПС выше максимально допустимого значения, необходимо либо увеличить (путем ручного ввода нужного значения) откачку нефти с ГНПС (столбец BE), либо уменьшить поступление нефти через СИКН-1208 [путем уменьшения ручным вводом наличия нефти в РП УПСВ-Ю (столбец F), УПСВ-С (столбец G), ЦПС (столбец H) до нужных показателей]"
            V_gnps.update({"status": 3, "message": msg})
    delta_gnps = V_gnps["value"] - V_gnps_prev
    if delta_gnps >= 0:
        if abs(delta_gnps) > delta_V_gnps_max:
            msg = "Скорость наполнения РП ГНПС больше допустимой величины, необходимо либо увеличить (путем ручного ввода нужного значения) откачку нефти с ГНПС (столбец BE), либо уменьшить поступление нефти через СИКН-1208 [путем увеличения ручным вводом наличия нефти в РП УПСВ-Ю (столбец F), УПСВ-С (столбец G), ЦПС (столбец H) до нужных показателей]"
            V_gnps.update({"status": 3, "message": msg})
    else:
        if abs(delta_gnps) > delta_VO_gnps_max:
            msg = "Скорость опорожнения РП больше допустимой величины, необходимо либо уменьшить (путем ручного ввода нужного значения) откачку нефти с ГНПС (столбец BE), либо увеличить поступление нефти через СИКН-1208 [путем увеличения ручным вводом наличия нефти в РП УПСВ-Ю (столбец F), УПСВ-С (столбец G), ЦПС (столбец H) до нужных показателей]"
            V_gnps.update({"status": 3, "message": msg})

    # --- 90. Проверка выполнения условий по наличию нефти на НПС-1
    V_nps_1 = {"value": (V_nps_1.get("value") if isinstance(V_nps_1, dict) else V_nps_1), "status": 0, "message": ""}
    if VA_nps_1_min <= V_nps_1["value"] <= VA_nps_1_max:
        V_nps_1.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти на НПС-1 выполнена"})
    else:
        if V_nps_1["value"] < VA_nps_1_min:
            msg = "Наличие нефти в РП НПС-1 ниже минимального допустимого значения, необходимо уменьшить откачку нефти с НПС-1 на НПС-2 путем увеличения (ручным вводом) наличия нефти в РП НПС-1 (столбец BG) до требуемого значения"
            V_nps_1.update({"status": 3, "message": msg})
        elif V_nps_1["value"] > VA_nps_1_max:
            msg = "Наличие нефти в РП НПС-1 выше максимально допустимого значения, необходимо увеличить откачку нефти с НПС-1 на НПС-2 путем увеличения (ручным вводом) наличия нефти в РП НПС-1 (столбец BG) до требуемого значения"
            V_nps_1.update({"status": 3, "message": msg})
    delta_nps_1 = V_nps_1["value"] - V_nps_1_prev
    if delta_nps_1 >= 0:
        if abs(delta_nps_1) > delta_V_nps_1_max:
            msg = "Скорость наполнения РП НПС-1 больше допустимой величины, необходимо увеличить откачку нефти с НПС-1 на НПС-2 путем уменьшения (ручным вводом) наличия нефти в РП НПС-1 (столбец BG) до требуемого значения"
            V_nps_1.update({"status": 3, "message": msg})
    else:
        if abs(delta_nps_1) > delta_VO_nps_1_max:
            msg = "Скорость опорожнения РП НПС-1 больше допустимой величины, необходимо уменьшить откачку нефти с НПС-1 на НПС-2 путем увеличения (ручным вводом) наличия нефти в РП НПС-1 (столбец BG) до требуемого значения"
            V_nps_1.update({"status": 3, "message": msg})

    # --- 91. Проверка выполнения условий по наличию нефти на НПС-2
    V_nps_2 = {"value": (V_nps_2.get("value") if isinstance(V_nps_2, dict) else V_nps_2), "status": 0, "message": ""}
    if VA_nps_2_min <= V_nps_2["value"] <= VA_nps_2_max:
        V_nps_2.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти на НПС-2 выполнена"})
    else:
        if V_nps_2["value"] < VA_nps_2_min:
            msg = "Наличие нефти в РП НПС-2 ниже минимального допустимого значения, необходимо уменьшить откачку нефти с НПС-1 на НПС-2 путем увеличения (ручным вводом) наличия нефти в РП НПС-2 до требуемого значения"
            V_nps_2.update({"status": 3, "message": msg})
        elif V_nps_2["value"] > VA_nps_2_max:
            msg = "Наличие нефти в РП НПС-2 выше максимально допустимого значения, необходимо увеличить откачку нефти с НПС-1 на НПС-2 путем уменьшения (ручным вводом) наличия нефти в РП НПС-2 до требуемого значения"
            V_nps_2.update({"status": 3, "message": msg})
    delta_nps_2 = V_nps_2["value"] - V_nps_2_prev
    if delta_nps_2 >= 0:
        if abs(delta_nps_2) > delta_V_nps_2_max:
            msg = "Скорость наполнения РП НПС-2 больше допустимой величины, необходимо увеличить откачку нефти с НПС-1 на НПС-2 путем уменьшения (ручным вводом) наличия нефти в РП НПС-2 до требуемого значения"
            V_nps_2.update({"status": 3, "message": msg})
    else:
        if abs(delta_nps_2) > delta_VO_nps_2_max:
            msg = "Скорость опорожнения РП НПС-2 больше допустимой величины, необходимо уменьшить откачку нефти с НПС-1 на НПС-2 путем увеличения (ручным вводом) наличия нефти в РП НПС-2 до требуемого значения"
            V_nps_2.update({"status": 3, "message": msg})
    # --- 92. Проверка выполнения условий по наличию нефти на КНПС
    V_knps = {"value": (V_knps.get("value") if isinstance(V_knps, dict) else V_knps), "status": 0, "message": ""}
    if VN_knps_min <= V_knps["value"] <= VA_knps_max:
        V_knps.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти на КНПС выполнена"})
    else:
        if V_knps["value"] < VN_knps_min:
            msg = "Наличие нефти в РП КНПС ниже минимального допустимого значения, необходимо уменьшить (ручным вводом) сдачу нефти АО «ВН» (столбец BX) в магистральный нефтепровод через СИКН 1209 "
            V_knps.update({"status": 3, "message": msg})
        elif V_knps["value"] > VA_knps_max:
            msg = "Наличие нефти в РП КНПС выше максимально допустимого значения, необходимо увеличить (ручным вводом) сдачу нефти АО «ВН» (столбец BX) в магистральный нефтепровод через СИКН 1209 "
            V_knps.update({"status": 3, "message": msg})
    delta_knps = V_knps["value"] - V_knps_prev
    if delta_knps >= 0:
        if abs(delta_knps) > delta_V_knps_max:
            msg = "Скорость наполнения РП КНПС больше допустимой величины, необходимо увеличить (ручным вводом) сдачу нефти АО «ВН» (столбец BX) в магистральный нефтепровод через СИКН 1209 "
            V_knps.update({"status": 3, "message": msg})
    else:
        if abs(delta_knps) > delta_VO_knps_max:
            msg = "Скорость опорожнения РП КНПС больше допустимой величины, необходимо уменьшить (ручным вводом) сдачу нефти АО «ВН» (столбец BX) в магистральный нефтепровод через СИКН 1209 "
            V_knps.update({"status": 3, "message": msg})
    # --- 93. Проверка наличия нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РВС УПН Лодочное
    V_ichem = {"value": (V_ichem.get("value") if isinstance(V_ichem, dict) else V_ichem), "status": 0, "message": ""}
    if V_ichem_min <= V_ichem["value"] <= V_ichem_max:
        V_ichem.update({"status": 1,
                            "message": "Проверка выполнения условий по наличию нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РВС УПН Лодочное"})
    else:
        if V_ichem["value"] < V_ichem_min:
            msg = "Наличие нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РВС УПН Лодочное ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) откачку нефти Ичемминского ЛУ в магистральный нефтепровод (столбец AW)"
            V_ichem.update({"status": 3, "message": msg})
        elif V_ichem["value"] > V_ichem_max:
            msg = "Наличие нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РВС УПН Лодочное больше максимально допустимого значения. Необходимо увеличить (ручным вводом) откачку нефти Ичемминского ЛУ в магистральный нефтепровод (столбец AW)"
            V_ichem.update({"status": 3, "message": msg})
    # --- 94. Проверка выполнения условий наличия нефти Лодочного ЛУ в РП на ЦПС и УПСВ-Юг
    V_lodochny_cps_upsv_yu = {"value": (V_lodochny_cps_upsv_yu.get("value") if isinstance(V_lodochny_cps_upsv_yu, dict) else V_lodochny_cps_upsv_yu), "status": 0, "message": ""}
    if V_lodochny_cps_upsv_yu["value"] >= 0:
        V_lodochny_cps_upsv_yu.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти Лодочного ЛУ в РП на ЦПС и УПСВ-ЮГ"})
    else:
        msg = "Значение наличия нефти Лодочного ЛУ на ЦПС и на УПСВ-Юг меньше нуля. Необходимо уменьшить откачку нефти ООО «Тагульское» на СИНК-1208 (столбец Р)."
        V_lodochny_cps_upsv_yu.update({"status": 3, "message": msg})
        if not G_sikn_tagul_is_manual:
            G_sikn_tagul = G_sikn_tagul - abs(V_lodochny_cps_upsv_yu["value"])
        
    # --- 95.	Проверка наличия нефти на объектах ЦТН по недропользователям
    V_tstn_vn = {"value": (V_tstn_vn.get("value") if isinstance(V_tstn_vn, dict) else V_tstn_vn), "status": 0, "message": ""}
    if V_tstn_vn_min <= V_tstn_vn["value"] <= V_tstn_vn_max:
        V_tstn_vn.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти АО «Ванкорнефть» на ЦТН"})
    else:
        if V_tstn_vn["value"] < V_tstn_vn_min:
            msg = "Наличие нефти АО «Ванкорнефть» в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти АО «ВН» через СИКН-1209 (столбец BX) до нужного значения"
            V_tstn_vn.update({"status": 3, "message": msg})
        elif V_tstn_vn["value"] > V_tstn_vn_max:
            msg = "Наличие нефти АО «Ванкорнефть» в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти АО «ВН» через СИКН-1209 (столбец BX) до нужного значения"
            V_tstn_vn.update({"status": 3, "message": msg})

    V_tstn_suzun = {"value": (V_tstn_suzun.get("value") if isinstance(V_tstn_suzun, dict) else V_tstn_suzun), "status": 0, "message": ""}
    if V_tstn_suzun_min <= V_tstn_suzun["value"] <= V_tstn_suzun_max:
        V_tstn_suzun.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти АО «Сузун» на ЦТН"})
    else:
        if V_tstn_suzun["value"] < V_tstn_suzun_min:
            msg = "Наличие нефти АО «Сузун» (Сузун) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти АО «Сузун» (Сузун) через СИКН-1209 (столбец BY) до нужного значения"
            V_tstn_suzun.update({"status": 3, "message": msg})
        elif V_tstn_suzun["value"] > V_tstn_suzun_max:
            msg = "Наличие нефти АО «Сузун» (Сузун) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти АО «Сузун» (Сузун) через СИКН-1209 (столбец BY) до нужного значения"
            V_tstn_suzun.update({"status": 3, "message": msg})

    V_tstn_suzun_vankor = {"value": (V_tstn_suzun_vankor.get("value") if isinstance(V_tstn_suzun_vankor, dict) else V_tstn_suzun_vankor), "status": 0, "message": ""}
    if V_tstn_suzun_vankor_min <= V_tstn_suzun_vankor["value"] <= V_tstn_suzun_vankor_max:
        V_tstn_suzun_vankor.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти АО «Сузун» (Ванкор) на ЦТН"})
    else:
        if V_tstn_suzun_vankor["value"] < V_tstn_suzun_vankor_min:
            msg = "Наличие нефти АО «Сузун» (Ванкор) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти АО «Сузун» (Ванкор) через СИКН-1209 (столбец BZ) до нужного значения"
            V_tstn_suzun_vankor.update({"status": 3, "message": msg})
        elif V_tstn_suzun_vankor["value"] > V_tstn_suzun_vankor_max:
            msg = "Наличие нефти АО «Сузун» (Ванкор) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти АО «Сузун» (Ванкор) через СИКН-1209 (столбец BZ) до нужного значения"
            V_tstn_suzun_vankor.update({"status": 3, "message": msg})

    V_tstn_suzun_vslu = {"value": (V_tstn_suzun_vslu.get("value") if isinstance(V_tstn_suzun_vslu, dict) else V_tstn_suzun_vslu), "status": 0, "message": ""}
    if V_tstn_suzun_vslu_min <= V_tstn_suzun_vslu["value"] <= V_tstn_suzun_vslu_max:
        V_tstn_suzun_vslu.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти АО «Сузун» (ВСЛУ) на ЦТН"})
    else:
        if V_tstn_suzun_vslu["value"] < V_tstn_suzun_vslu_min:
            msg = "Наличие нефти АО «Сузун» (ВСЛУ) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти АО «Сузун» (ВСЛУ) через СИКН-1209 (столбец CA) до нужного значения"
            V_tstn_suzun_vslu.update({"status": 3, "message": msg})
        elif V_tstn_suzun_vslu["value"] > V_tstn_suzun_vslu_max:
            msg = "Наличие нефти АО «Сузун» (ВСЛУ) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти АО «Сузун» (ВСЛУ) через СИКН-1209 (столбец CA) до нужного значения"
            V_tstn_suzun_vslu.update({"status": 3, "message": msg})

    V_tstn_tagul_obsh = {"value": (V_tstn_tagul_obsh.get("value") if isinstance(V_tstn_tagul_obsh, dict) else V_tstn_tagul_obsh), "status": 0, "message": ""}
    if V_tstn_tagul_obsh_min <= V_tstn_tagul_obsh["value"] <= V_tstn_tagul_obsh_max:
        V_tstn_tagul_obsh.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти ООО «Тагульское» (всего) на ЦТН"})
    else:
        if V_tstn_tagul_obsh["value"] < V_tstn_tagul_obsh_min:
            msg = "Наличие нефти ООО «Тагульское» (всего) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «Тагульское» (Лодочный ЛУ) (столбец CC), ООО «Тагульское» (Тагульский ЛУ) (столбец CD) через СИКН-1209 до нужного значения"
            V_tstn_tagul_obsh.update({"status": 3, "message": msg})
        elif V_tstn_tagul_obsh["value"] > V_tstn_tagul_obsh_max:
            msg = "Наличие нефти ООО «Тагульское» (всего) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «Тагульское» (Лодочный ЛУ) (столбец CC), ООО «Тагульское» (Тагульский ЛУ) (столбец CD) через СИКН-1209 до нужного значения"
            V_tstn_tagul_obsh.update({"status": 3, "message": msg})

    V_tstn_lodochny = {"value": (V_tstn_lodochny.get("value") if isinstance(V_tstn_lodochny, dict) else V_tstn_lodochny), "status": 0, "message": ""}
    if V_tstn_lodochny_min <= V_tstn_lodochny["value"] <= V_tstn_lodochny_max:
        V_tstn_lodochny.update({"status": 1,
                                    "message": "Проверка выполнения условий по наличию нефти ООО «Тагульское» (Лодочный ЛУ) на ЦТН"})
    else:
        if V_tstn_lodochny["value"] < V_tstn_lodochny_min:
            msg = "Наличие нефти ООО «Тагульское» (Лодочный ЛУ) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «Тагульское» (Лодочный ЛУ) (столбец CC) через СИКН-1209 до нужного значения"
            V_tstn_lodochny.update({"status": 3, "message": msg})
        elif V_tstn_lodochny["value"] > V_tstn_lodochny_max:
            msg = "Наличие нефти ООО «Тагульское» (Лодочный ЛУ) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «Тагульское» (Лодочный ЛУ) (столбец CC)  через СИКН-1209 до нужного значения"
            V_tstn_lodochny.update({"status": 3, "message": msg})

    V_tstn_tagul = {"value": (V_tstn_tagul.get("value") if isinstance(V_tstn_tagul, dict) else V_tstn_tagul), "status": 0, "message": ""}
    if V_tstn_tagul_min <= V_tstn_tagul["value"] <= V_tstn_tagul_max:
        V_tstn_tagul.update({"status": 1,
                                 "message": "Проверка выполнения условий по наличию нефти ООО «Тагульское» (Тагульский ЛУ) на ЦТН"})
    else:
        if V_tstn_tagul["value"] < V_tstn_tagul_min:
            msg = "Наличие нефти ООО «Тагульское» (Тагульский ЛУ) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «Тагульское» (Тагульский ЛУ) (столбец CD) через СИКН-1209 до нужного значения"
            V_tstn_tagul.update({"status": 3, "message": msg})
        elif V_tstn_tagul["value"] > V_tstn_tagul_max:
            msg = "Наличие нефти ООО «Тагульское» (Тагульский ЛУ) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «Тагульское» (Тагульский ЛУ) (столбец CD) через СИКН-1209 до нужного значения"
            V_tstn_tagul.update({"status": 3, "message": msg})

    V_tstn_skn = {"value": (V_tstn_skn.get("value") if isinstance(V_tstn_skn, dict) else V_tstn_skn), "status": 0, "message": ""}
    if V_tstn_skn_min <= V_tstn_skn["value"] <= V_tstn_skn_max:
        V_tstn_skn.update(
            {"status": 1, "message": "Проверка выполнения условий по наличию нефти ООО «СевКомНефтегаз» на ЦТН"})
    else:
        if V_tstn_skn["value"] < V_tstn_skn_min:
            msg = "Наличие нефти ООО «СевКомНефтегаз» в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «СевКомНефтегаз» через СИКН-1209 (столбец CE) до нужного значения."
            V_tstn_skn.update({"status": 3, "message": msg})
        elif V_tstn_skn["value"] > V_tstn_skn_max:
            msg = "Наличие нефти ООО «СевКомНефтегаз» в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «СевКомНефтегаз» через СИКН-1209 (столбец CE) до нужного значения."
            V_tstn_skn.update({"status": 3, "message": msg})

    V_tstn_vo = {"value": (V_tstn_vo.get("value") if isinstance(V_tstn_vo, dict) else V_tstn_vo), "status": 0, "message": ""}
    if V_tstn_vo_min <= V_tstn_vo["value"] <= V_tstn_vo_max:
        V_tstn_vo.update({"status": 1,
                              "message": "Проверка выполнения условий по наличию нефти ООО «Восток Ойл» (Ичемминский ЛУ) на ЦТН"})
    else:
        if V_tstn_vo["value"] < V_tstn_vo_min:
            msg = "Наличие нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «Восток Ойл» (Ичемминский ЛУ) через СИКН-1209 (столбец CF) до нужного значения"
            V_tstn_vo.update({"status": 3, "message": msg})
        elif V_tstn_vo["value"] > V_tstn_vo_max:
            msg = "Наличие нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «Восток Ойл» (Ичемминский ЛУ) через СИКН-1209 (столбец CF) до нужного значения"
            V_tstn_vo.update({"status": 3, "message": msg})

    V_tstn_tng = {"value": (V_tstn_tng.get("value") if isinstance(V_tstn_tng, dict) else V_tstn_tng), "status": 0, "message": ""}
    if V_tstn_tng_min <= V_tstn_tng["value"] <= V_tstn_tng_max:
        V_tstn_tng.update({"status": 1,
                               "message": "Проверка выполнения условий по наличию нефти АО «Таймырнефтегаз» (Пайяхский ЛУ) на ЦТН"})
    else:
        if V_tstn_tng["value"] < V_tstn_tng_min:
            msg = "Наличие нефти АО «Таймырнефтегаз» (Пайяхский ЛУ) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти АО «Таймырнефтегаз» (Пайяхский ЛУ) через СИКН-1209 (столбец CG) до нужного значения"
            V_tstn_tng.update({"status": 3, "message": msg})
        elif V_tstn_tng["value"] > V_tstn_tng_max:
            msg = "Наличие нефти АО «Таймырнефтегаз» (Пайяхский ЛУ) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти АО «Таймырнефтегаз» (Пайяхский ЛУ) через СИКН-1209 (столбец CG) до нужного значения"
            V_tstn_tng.update({"status": 3, "message": msg})

    V_tstn_kchng = {"value": (V_tstn_kchng.get("value") if isinstance(V_tstn_kchng, dict) else V_tstn_kchng), "status": 0, "message": ""}
    if V_tstn_kchng_min <= V_tstn_kchng["value"] <= V_tstn_kchng_max:
        V_tstn_kchng.update({"status": 1,
                                 "message": "Проверка выполнения условий по наличию нефти ООО «КЧНГ» (Русско-Реченское месторождение) на ЦТН"})
    else:
        if V_tstn_kchng["value"] < V_tstn_kchng_min:
            msg = "Наличие нефти ООО «КЧНГ» (Русско-Реченское месторождение) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «КЧНГ» (Русско-Реченское месторождение) через СИКН-1209 (столбец CH) до нужного значения."
            V_tstn_kchng.update({"status": 3, "message": msg})
        elif V_tstn_kchng["value"] > V_tstn_kchng_max:
            msg = "Наличие нефти ООО «КЧНГ» (Русско-Реченское месторождение)в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «КЧНГ» (Русско-Реченское месторождение) через СИКН-1209 (столбец CH) до нужного значения"
            V_tstn_kchng.update({"status": 3, "message": msg})

    # --- 96. Проверка соблюдения нормативных значений насосного оборудования ГНПС
    Q_gnps = G_gnps / p_gnps / 24

    Q_gnps = {"value": Q_gnps, "status": 0, "message": ""}
    if Q_gnps["value"] < Q_gnps_min1:
        msg = "Расход нефти на насосы ГНПС ниже минимально допустимого значения. Необходимо увеличить (ручным вводом) откачку нефти с ГНПС (столбец BE) до нужного значения"
        Q_gnps.update({"status": 3, "message": msg})
    elif Q_gnps["value"] > Q_gnps_max2:
        msg = "Расход нефти на насосы ГНПС больше максимально допустимого значения. Необходимо уменьшить (ручным вводом) откачку нефти с ГНПС (столбец BE) до нужного значения"
        Q_gnps.update({"status": 3, "message": msg})
    elif Q_gnps["value"] <= Q_gnps_max1:
        Q_gnps.update({"status": 1, "message": "Режим работы насосного оборудования 1-1-1"})
    else:
        Q_gnps.update({"status": 1,
                           "message": "Режим работы насосного оборудования 2-2-2. Рекомендуется перераспределить объемы перекачиваемой нефти."})
    # --- 97. Проверка соблюдения нормативных значений насосного оборудования ГНПС
    Q_nps_1_2 = (G_gnps + G_tagul_lodochny + V_nps_1["value"] - V_nps_1_prev + V_nps_2["value"] - V_nps_2_prev) / p_nps_1_2 / 24
    Q_nps_1_2 = {"value": Q_nps_1_2, "status": 0, "message": ""}
    if Q_nps_1_2["value"] < Q_nps_1_2_min1:
        msg = "Расход нефти на насосы НПС-1, НПС-2 ниже минимально допустимого значения. Необходимо увеличить (ручным вводом) откачку нефти с ГНПС (столбец BE) до нужного значения"
        Q_nps_1_2.update({"status": 3, "message": msg})
    elif Q_nps_1_2["value"] > Q_nps_1_2_max2:
        msg = "Расход нефти на насосы НПС-1, НПС-2 больше максимально допустимого значения. Необходимо уменьшить (ручным вводом) откачку нефти с ГНПС (столбец BE) до нужного значения"
        Q_nps_1_2.update({"status": 3, "message": msg})
    elif Q_nps_1_2["value"] <= Q_nps_1_2_max1:
        Q_nps_1_2.update({"status": 1, "message": "Режим работы насосного оборудования 1-1-1"})
    else:
        Q_nps_1_2.update({"status": 1,
                              "message": "Режим работы насосного оборудования 2-2-2. Рекомендуется перераспределить объемы перекачиваемой нефти."})
    # --- 98. Проверка соблюдения нормативных значений насосного оборудования КНПС
    Q_knps = F / p_knps / 24
    Q_knps = {"value": Q_knps, "status": 0, "message": ""}
    if Q_knps["value"] < Q_knps_min1:
        msg = "Расход нефти на насосы КНПС ниже минимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти через СИКН-1209 (столбцы BX-CH) до нужного значения "
        Q_knps.update({"status": 3, "message": msg})
    elif Q_knps["value"] > Q_knps_max2:
        msg = "Расход нефти на насосы КНПС больше максимально допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти через СИКН-1209 (столбцы BX-CH) до нужного значения "
        Q_knps.update({"status": 3, "message": msg})
    elif Q_knps["value"] <= Q_knps_max1:
        Q_knps.update({"status": 1, "message": "Режим работы насосного оборудования 1-1-1"})
    else:
        Q_knps.update({"status": 1,
                           "message": "Режим работы насосного оборудования 2-2-2. Рекомендуется рассмотреть возможность перераспределения перекачиваемой нефти по дням."})
    return {
        "V_upsv_yu": V_upsv_yu,
        "V_upsv_s": V_upsv_s,
        "V_cps": V_cps,
        "V_upn_suzun": V_upn_suzun,
        "V_upn_lodochny": V_upn_lodochny,
        "V_tagul_tr": V_tagul_tr,
        "V_gnps": V_gnps,
        "V_nps_1": V_nps_1,
        "V_nps_2": V_nps_2,
        "V_knps": V_knps,
        "V_ichem": V_ichem,
        "V_lodochny_cps_upsv_yu": V_lodochny_cps_upsv_yu,
        "V_tstn_vn": V_tstn_vn,
        "V_tstn_suzun": V_tstn_suzun,
        "V_tstn_suzun_vankor": V_tstn_suzun_vankor,
        "V_tstn_suzun_vslu": V_tstn_suzun_vslu,
        "V_tstn_tagul_obsh": V_tstn_tagul_obsh,
        "V_tstn_lodochny": V_tstn_lodochny,
        "V_tstn_tagul": V_tstn_tagul,
        "V_tstn_skn": V_tstn_skn,
        "V_tstn_vo": V_tstn_vo,
        "V_tstn_tng": V_tstn_tng,
        "V_tstn_kchng": V_tstn_kchng,
        "Q_gnps": Q_gnps,
        "Q_nps_1_2": Q_nps_1_2,
        "Q_knps": Q_knps,
        "F": F,
    }

def deviations_from_bp_calc(
        F_suzun_vankor_sum, F_tagul_lpu_sum, F_tagul_tpu_sum, F_vn_sum, F_skn_sum, F_vo_sum, F_tng_sum, F_kchng_sum, F_suzun_vslu_sum,
        F_suzun_sum, F_bp_tagul_lpu_month, F_bp_tagul_tpu_month, F_bp_suzun_vankor_month, F_bp_suzun_vslu_month, F_bp_skn_month, F_bp_vo_month,
        F_bp_tng_month, F_bp_kchng_month, F_bp_suzun_month, F_bp_vn_month
):
    def _wrap_delta(value):
        """
        0 - значение равняется 0
        1 - значение больше 0
        2 - значение меньше нуля
        """
        try:
            v = float(value)
        except (TypeError, ValueError):
            v = 0.0

        # чтобы избежать -0.0 хвостов float
        if abs(v) < 1e-9:
            v = 0.0

        if v == 0.0:
            status = 0
        elif v > 0.0:
            status = 1
        else:
            status = 2
        return {"value": v, "status": status, "message": None}

    delta_F_suzun_vankor = F_suzun_vankor_sum - F_bp_suzun_vankor_month
    delta_F_tagul_lpu = F_tagul_lpu_sum - F_bp_tagul_lpu_month
    delta_F_tagul_tpu = F_tagul_tpu_sum - F_bp_tagul_tpu_month
    delta_F_tagul = delta_F_tagul_lpu + delta_F_tagul_tpu
    delta_F_vn = F_vn_sum - F_bp_vn_month
    delta_F_skn = F_skn_sum - F_bp_skn_month
    delta_F_vo = F_vo_sum - F_bp_vo_month
    delta_F_tng = F_tng_sum - F_bp_tng_month
    delta_F_kchng = F_kchng_sum - F_bp_kchng_month
    delta_F_suzun_vslu = F_suzun_vslu_sum - F_bp_suzun_vslu_month
    delta_F_suzun = F_suzun_sum - F_bp_suzun_month
    delta_F = delta_F_suzun_vankor + delta_F_tagul_lpu + delta_F_tagul_tpu + delta_F_tagul + delta_F_vn + delta_F_skn + delta_F_vo + delta_F_tng + delta_F_kchng + delta_F_suzun_vslu + delta_F_suzun



    delta_F_suzun_vankor = _wrap_delta(delta_F_suzun_vankor)
    delta_F_tagul_lpu = _wrap_delta(delta_F_tagul_lpu)
    delta_F_tagul_tpu = _wrap_delta(delta_F_tagul_tpu)
    delta_F_tagul = _wrap_delta(delta_F_tagul)
    delta_F_vn = _wrap_delta(delta_F_vn)
    delta_F_skn = _wrap_delta(delta_F_skn)
    delta_F_vo = _wrap_delta(delta_F_vo)
    delta_F_tng = _wrap_delta(delta_F_tng)
    delta_F_kchng = _wrap_delta(delta_F_kchng)
    delta_F_suzun_vslu = _wrap_delta(delta_F_suzun_vslu)
    delta_F_suzun = _wrap_delta(delta_F_suzun)
    delta_F = _wrap_delta(delta_F)
    
    return{
        "delta_F_suzun_vankor":delta_F_suzun_vankor,
        "delta_F_tagul_lpu":delta_F_tagul_lpu,
        "delta_F_tagul_tpu":delta_F_tagul_tpu,
        "delta_F_tagul":delta_F_tagul,
        "delta_F_vn":delta_F_vn,
        "delta_F":delta_F,
        "delta_F_skn":delta_F_skn,
        "delta_F_vo":delta_F_vo,
        "delta_F_tng":delta_F_tng,
        "delta_F_kchng":delta_F_kchng,
        "delta_F_suzun_vslu":delta_F_suzun_vslu,
        "delta_F_suzun":delta_F_suzun,
    }

def planned_balance_for_bp_vn_calc(
        V_vn_ost_np_nm, V_vn_ost_app_nm, V_vn_ost_tech_nm, V_vn_path_nm, Q_vn_oil, Q_vn_condensate, V_vn_lost_oil, V_vn_lost_cond, G_vn_fuel, G_vn_fill,
        V_vn_lost_transp, G_vn_release_rn_drillig, G_vn_release_suzun, G_vn_release_well_service, V_vn_ost_np_km, V_vn_ost_app_km, V_vn_ost_tech_km, V_vn_path_km,
        F_vn_total
):
    # Остатки нефти на ВПУ на начало месяца
    V_vn_ost_vpy_nm = V_vn_ost_np_nm + V_vn_ost_app_nm + V_vn_ost_tech_nm
# Остатки нефти (газового конденсата) на начало месяца, всего
    V_vn_ost_nm = V_vn_ost_vpy_nm + V_vn_path_nm
# Добыча нефти (газового конденсата)
    Q_vn_total = Q_vn_oil + Q_vn_condensate
#  Технологические потери нефти (газового конденсата)
    V_vn_lost = V_vn_lost_oil + V_vn_lost_cond + V_vn_lost_transp
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_vn_own = G_vn_fuel + G_vn_fill
# Отпуск нефти (газового конденсата), всего
    G_vn_release = G_vn_release_rn_drillig + G_vn_release_suzun + G_vn_release_well_service
# Остатки нефти на ВПУ на конец месяца
    V_vn_ost_vpy_km = V_vn_ost_np_km + V_vn_ost_app_km + V_vn_ost_tech_km
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_vn_ost_km = V_vn_ost_vpy_km + V_vn_path_km
# Изменение остатков нефти (газового конденсата) собственных, всего
    V_vn_delta_ost = V_vn_ost_km - V_vn_ost_nm
# Выполнение процедуры проверки
    V_vn_check = (V_vn_ost_nm + Q_vn_total) - (V_vn_lost + G_vn_own + G_vn_release + F_vn_total + V_vn_ost_km)
    if V_vn_check != 0:
        _status = 2
        _message = "Проверка не пройдена"
    else:
        _status = 1
        _message = "Проверка пройдена"
    return{
        "V_vn_check":{"value": V_vn_check, "status": _status, "message": _message},
        "V_vn_delta_ost":{"value": V_vn_delta_ost, "status": _status, "message": _message},
        "V_vn_ost_km":{"value": V_vn_ost_km, "status": _status, "message": _message},
        "V_vn_ost_vpy_km":{"value": V_vn_ost_vpy_km, "status": _status, "message": _message},
        "G_vn_release":{"value": G_vn_release, "status": _status, "message": _message},
        "G_vn_own":{"value": G_vn_own, "status": _status, "message": _message},
        "V_vn_lost":{"value": V_vn_lost, "status": _status, "message": _message},
        "Q_vn_total":{"value": Q_vn_total, "status": _status, "message": _message},
        "V_vn_ost_nm":{"value": V_vn_ost_nm, "status": _status, "message": _message},
        "V_vn_ost_vpy_nm":{"value": V_vn_ost_vpy_nm, "status": _status, "message": _message},
    }

def planned_balance_for_bp_suzun_calc(
        V_suzun_ost_np_nm, V_suzun_ost_app_nm, V_suzun_ost_tech_nm, V_suzun_path_nm, Q_suzun_oil, Q_suzun_condensate, V_suzun_lost_oil, V_suzun_lost_transp_vankor,
        V_suzun_lost_transp_suzun, G_suzun_release_rn_drillig, V_suzun_ost_np_km, V_suzun_ost_app_km, V_suzun_ost_tech_km, V_suzun_path_km,
        F_suzun_total, G_suzun_mupn, F_suzun_vankor_total, G_suzun_buy
):
    # Остатки нефти на ВПУ на начало месяца
    V_suzun_ost_spy_nm = V_suzun_ost_np_nm + V_suzun_ost_app_nm + V_suzun_ost_tech_nm
# Остатки нефти (газового конденсата) на начало месяца, всего
    V_suzun_ost_nm = V_suzun_ost_spy_nm + V_suzun_path_nm
# Добыча нефти (газового конденсата)
    Q_suzun_total = Q_suzun_oil + Q_suzun_condensate
#  Технологические потери нефти (газового конденсата)
    V_suzun_lost = V_suzun_lost_oil + V_suzun_lost_transp_vankor + V_suzun_lost_transp_suzun
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_suzun_own = G_suzun_mupn
# Отпуск нефти (газового конденсата), всего
    G_suzun_release = G_suzun_release_rn_drillig
    F_suzun_suzun = F_suzun_total - F_suzun_vankor_total
# Остатки нефти на ВПУ на конец месяца
    V_suzun_ost_spy_km = V_suzun_ost_np_km + V_suzun_ost_app_km + V_suzun_ost_tech_km
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_suzun_ost_km = V_suzun_ost_spy_km + V_suzun_path_km
# Изменение остатков нефти (газового конденсата) собственных, всего
    V_suzun_delta_ost = V_suzun_ost_km - V_suzun_ost_nm
# Выполнение процедуры проверки
    V_suzun_check = (V_suzun_ost_nm + Q_suzun_total + G_suzun_buy) - (V_suzun_lost + G_suzun_own + G_suzun_release + F_suzun_total + V_suzun_ost_km)
    if V_suzun_check != 0:
        _status = 2
        _message = "Проверка не пройдена"
    else:
        _status = 1
        _message = "Проверка пройдена"
    return{
        "V_suzun_check":{"value": V_suzun_check, "status": _status, "message": _message},
        "V_suzun_delta_ost":{"value": V_suzun_delta_ost, "status": _status, "message": _message},
        "V_suzun_ost_km":{"value": V_suzun_ost_km, "status": _status, "message": _message},
        "V_suzun_ost_spy_km":{"value": V_suzun_ost_spy_km, "status": _status, "message": _message},
        "G_suzun_release":{"value": G_suzun_release, "status": _status, "message": _message},
        "G_suzun_own":{"value": G_suzun_own, "status": _status, "message": _message},
        "V_suzun_lost":{"value": V_suzun_lost, "status": _status, "message": _message},
        "Q_suzun_total":{"value": Q_suzun_total, "status": _status, "message": _message},
        "V_suzun_ost_nm":{"value": V_suzun_ost_nm, "status": _status, "message": _message},
        "V_suzun_ost_spy_nm":{"value": V_suzun_ost_spy_nm, "status": _status, "message": _message},
        "F_suzun_suzun":{"value": F_suzun_suzun, "status": _status, "message": _message},
    }

def planned_balance_for_bp_vo_calc(
        V_vo_ost_np_nm, V_vo_ost_app_nm, V_vo_ost_tech_nm, V_vo_path_nm, Q_vo_oil, Q_vo_condensate, V_vo_lost_oil, V_vo_lost_cond, G_vo_fuel, G_vo_fill,
        V_vo_lost_transp, G_vo_release, V_vo_ost_np_km, V_vo_ost_app_km, V_vo_ost_tech_km, V_vo_path_km,
        F_vo_total
):
    # Остатки нефти на ВПУ на начало месяца
    V_vo_ost_vpy_nm = V_vo_ost_np_nm + V_vo_ost_app_nm + V_vo_ost_tech_nm
# Остатки нефти (газового конденсата) на начало месяца, всего
    V_vo_ost_nm = V_vo_ost_vpy_nm + V_vo_path_nm
# Добыча нефти (газового конденсата)
    Q_vo_total = Q_vo_oil + Q_vo_condensate
#  Технологические потери нефти (газового конденсата)
    V_vo_lost = V_vo_lost_oil + V_vo_lost_cond + V_vo_lost_transp
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_vo_own = G_vo_fuel + G_vo_fill
# Остатки нефти на ВПУ на конец месяца
    V_vo_ost_vpy_km = V_vo_ost_np_km + V_vo_ost_app_km + V_vo_ost_tech_km
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_vo_ost_km = V_vo_ost_vpy_km + V_vo_path_km
# Изменение остатков нефти (газового конденсата) собственных, всего
    V_vo_delta_ost = V_vo_ost_km - V_vo_ost_nm
# Выполнение процедуры проверки
    V_vo_check = (V_vo_ost_nm + Q_vo_total) - (V_vo_lost + G_vo_own + G_vo_release + F_vo_total + V_vo_ost_km)
    if V_vo_check != 0:
        _status = 2
        _message = "Проверка не пройдена"
    else:
        _status = 1
        _message = "Проверка пройдена"

    return{
        "V_vo_check":{"value": V_vo_check, "status": _status, "message": _message},
        "V_vo_delta_ost":{"value": V_vo_delta_ost, "status": _status, "message": _message},
        "V_vo_ost_km":{"value": V_vo_ost_km, "status": _status, "message": _message},
        "V_vo_ost_vpy_km":{"value": V_vo_ost_vpy_km, "status": _status, "message": _message},
        "G_vo_own":{"value": G_vo_own, "status": _status, "message": _message},
        "V_vo_lost":{"value": V_vo_lost, "status": _status, "message": _message},
        "Q_vo_total":{"value": Q_vo_total, "status": _status, "message": _message},
        "V_vo_ost_nm":{"value": V_vo_ost_nm, "status": _status, "message": _message},
        "V_vo_ost_vpy_nm":{"value": V_vo_ost_vpy_nm, "status": _status, "message": _message},
    }

def planned_balance_for_bp_lodochny_calc(
        V_lodochny_ost_np_nm, V_lodochny_ost_app_nm, V_lodochny_ost_tech_nm, V_lodochny_path_nm, Q_lodochny_oil, Q_lodochny_condensate, V_lodochny_lost_oil, V_lodochny_lost_transp, G_lodochny_fuel,
        G_lodochny_release_rn_drillig, V_lodochny_ost_np_km, V_lodochny_ost_app_km, V_lodochny_ost_tech_km, V_lodochny_path_km, F_lodochny_total
):
    # Остатки нефти на ВПУ на начало месяца
    V_lodochny_ost_lpy_nm = V_lodochny_ost_np_nm + V_lodochny_ost_app_nm + V_lodochny_ost_tech_nm
# Остатки нефти (газового конденсата) на начало месяца, всего
    V_lodochny_ost_nm = V_lodochny_ost_lpy_nm + V_lodochny_path_nm
# Добыча нефти (газового конденсата)
    Q_lodochny_total = Q_lodochny_oil + Q_lodochny_condensate
#  Технологические потери нефти (газового конденсата)
    V_lodochny_lost = V_lodochny_lost_oil + V_lodochny_lost_transp
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_lodochny_own = G_lodochny_fuel
# Отпуск нефти (газового конденсата), всего
    G_lodochny_release = G_lodochny_release_rn_drillig
# Остатки нефти на ВПУ на конец месяца
    V_lodochny_ost_lpy_km = V_lodochny_ost_np_km + V_lodochny_ost_app_km + V_lodochny_ost_tech_km
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_lodochny_ost_km = V_lodochny_ost_lpy_km + V_lodochny_path_km
# Изменение остатков нефти (газового конденсата) собственных, всего
    V_lodochny_delta_ost = V_lodochny_ost_km - V_lodochny_ost_nm
# Выполнение процедуры проверки
    V_lodochny_check = (V_lodochny_ost_nm + Q_lodochny_total) - (V_lodochny_lost + G_lodochny_own + G_lodochny_release + F_lodochny_total + V_lodochny_ost_km)
    if V_lodochny_check != 0:
        _status = 2
        _message = "Проверка не пройдена"
    else:
        _status = 1
        _message = "Проверка пройдена"
    return{
        "V_lodochny_check":{"value": V_lodochny_check, "status": _status, "message": _message},
        "V_lodochny_delta_ost":{"value": V_lodochny_delta_ost, "status": _status, "message": _message},
        "V_lodochny_ost_km":{"value": V_lodochny_ost_km, "status": _status, "message": _message},
        "V_lodochny_ost_lpy_km":{"value": V_lodochny_ost_lpy_km, "status": _status, "message": _message},
        "G_lodochny_release":{"value": G_lodochny_release, "status": _status, "message": _message},
        "G_lodochny_own":{"value": G_lodochny_own, "status": _status, "message": _message},
        "V_lodochny_lost":{"value": V_lodochny_lost, "status": _status, "message": _message},
        "Q_lodochny_total":{"value": Q_lodochny_total, "status": _status, "message": _message},
        "V_lodochny_ost_nm":{"value": V_lodochny_ost_nm, "status": _status, "message": _message},
        "V_lodochny_ost_lpy_nm":{"value": V_lodochny_ost_lpy_nm, "status": _status, "message": _message},
    }

def planned_balance_for_bp_tagul_calc(
        V_tagul_ost_np_nm, V_tagul_ost_app_nm, V_tagul_ost_tech_nm, V_tagul_path_nm, Q_tagul_oil, Q_tagul_condensate, V_tagul_lost_oil, V_tagul_lost_transp, G_tagul_fuel,
        G_tagul_release_rn_drillig, G_tagul_release_vpt_neftmash, V_tagul_ost_np_km, V_tagul_ost_app_km, V_tagul_ost_tech_km, V_tagul_path_km,
        F_tagul_total
):
    # Остатки нефти на ВПУ на начало месяца
    V_tagul_ost_tpy_nm = V_tagul_ost_np_nm + V_tagul_ost_app_nm + V_tagul_ost_tech_nm
# Остатки нефти (газового конденсата) на начало месяца, всего
    V_tagul_ost_nm = V_tagul_ost_tpy_nm + V_tagul_path_nm
# Добыча нефти (газового конденсата)
    Q_tagul_total = Q_tagul_oil + Q_tagul_condensate
#  Технологические потери нефти (газового конденсата)
    V_tagul_lost = V_tagul_lost_oil + V_tagul_lost_transp
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_tagul_own = G_tagul_fuel
# Отпуск нефти (газового конденсата), всего
    G_tagul_release = G_tagul_release_rn_drillig + G_tagul_release_vpt_neftmash
# Остатки нефти на ВПУ на конец месяца
    V_tagul_ost_tpy_km = V_tagul_ost_np_km + V_tagul_ost_app_km + V_tagul_ost_tech_km
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_tagul_ost_km = V_tagul_ost_tpy_km + V_tagul_path_km
# Изменение остатков нефти (газового конденсата) собственных, всего
    delta_V_tagul_ost = V_tagul_ost_km - V_tagul_ost_nm
# Выполнение процедуры проверки
    V_tagul_check = (V_tagul_ost_nm + Q_tagul_total) - (V_tagul_lost + G_tagul_own + G_tagul_release + F_tagul_total + V_tagul_ost_km)
    if V_tagul_check != 0:
        _status = 2
        _message = "Проверка не пройдена"
    else:
        _status = 1
        _message = "Проверка пройдена"
    return{
        "V_tagul_check":{"value": V_tagul_check, "status": _status, "message": _message},
        "delta_V_tagul_ost":{"value": delta_V_tagul_ost, "status": _status, "message": _message},
        "V_tagul_ost_km":{"value": V_tagul_ost_km, "status": _status, "message": _message},
        "V_tagul_ost_tpu_km":{"value": V_tagul_ost_tpy_km, "status": _status, "message": _message},
        "G_tagul_release":{"value": G_tagul_release, "status": _status, "message": _message},
        "G_tagul_own":{"value": G_tagul_own, "status": _status, "message": _message},
        "V_tagul_lost":{"value": V_tagul_lost, "status": _status, "message": _message},
        "Q_tagul_total":{"value": Q_tagul_total, "status": _status, "message": _message},
        "V_tagul_ost_nm":{"value": V_tagul_ost_nm, "status": _status, "message": _message},
        "V_tagul_ost_tpy_nm":{"value": V_tagul_ost_tpy_nm, "status": _status, "message": _message},
    }

def planned_balance_for_bp_vn_gtm_calc(
        V_cppn_1_0, V_vn_gtm_ost_dead_nm, V_tstn_vn_0, V_vn_gtm_ost_np_nm, V_vn_gtm_ost_app_nm, Q_vankor_month, Q_vn_gtm_condensate, F_vn_total, K_vn_prod,
        K_vankor, V_vn_gtm_lost_condensate, G_vn_gtm_fuel, G_vn_gtm_fill, G_buying_oil_month, G_tagul_gtm_release_tbs, G_vn_gtm_release_rn_drillig, V_cppn_1,
        V_vn_gtm_ost_rvs_clean_nm, V_vn_gtm_ost_tov_nm, V_tstn_vn
):
    V_vn_gtm_ost_texn_nm = V_cppn_1_0
# Остатки нефти в резервуарах ВПУ на начало месяца отчетного периода
    V_vn_gtm_ost_rvs_nm = V_vn_gtm_ost_dead_nm + V_vn_gtm_ost_texn_nm
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор») на начало месяца отчетного периода
    V_vn_gtm_path_nm = V_tstn_vn_0
# Остатки нефти (газового конденсата) на ВПУ
    V_vn_gtm_ost_vpy_nm = V_vn_gtm_ost_np_nm + V_vn_gtm_ost_app_nm + V_vn_gtm_ost_rvs_nm
# Остатки нефти (газового конденсата) АО «Ванкорнефть», всего
    V_vn_gtm_ost_nm = V_vn_gtm_ost_vpy_nm + V_vn_gtm_path_nm
# Добыча нефти (газового конденсата) АО «Ванкорнефть», всего
    Q_vn_gtm_total = Q_vankor_month
# Добыча нефти АО «Ванкорнефть»
    Q_vn_gtm_oil = Q_vn_gtm_total - Q_vn_gtm_condensate
# Сдача нефти АО «Ванкорнефть»
    F_vn_gtm_total = F_vn_total
# Технологические потери нефти при добыче и подготовке
    V_vn_gtm_lost_oil = Q_vn_gtm_total * (K_vn_prod/100)
#  Технологические потери нефти (газового конденсата) при транспортировке
    V_vn_gtm_lost_transport = round(F_vn_gtm_total * (K_vankor/100))
# Технологические потери нефти (газового конденсата), всего
    V_vn_gtm_lost = V_vn_gtm_lost_oil + V_vn_gtm_lost_condensate + V_vn_gtm_lost_transport
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_vn_gtm_own = G_vn_gtm_fuel + G_vn_gtm_fill
# Отпуск нефти АО «Сузун»
    G_vn_gtm_release_suzun = G_buying_oil_month
# Отпуск нефти (газового конденсата) АО «Ванкорнефть», всего
    G_vn_gtm_release = G_tagul_gtm_release_tbs + G_vn_gtm_release_rn_drillig + G_vn_gtm_release_suzun
# Остатки нефти на ВПУ в нефтепроводах на конец месяца
    V_vn_gtm_ost_np_km = V_vn_gtm_ost_np_nm
# Технологические остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_vn_gtm_ost_texn_km = V_cppn_1
# Мертвые остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_vn_gtm_ost_dead_km = V_vn_gtm_ost_dead_nm
    V_vn_gtm_ost_app_km = V_vn_gtm_ost_app_nm
# Остатки нефти в РВС очистных сооружений на конец месяца отчетного периода
    V_vn_gtm_ost_rvs_clean_km = V_vn_gtm_ost_rvs_clean_nm
# Товарный остатки нефти на конец месяца отчетного периода
    V_vn_gtm_ost_tov_km = V_vn_gtm_ost_tov_nm
# Остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_vn_gtm_ost_rvs_km = V_vn_gtm_ost_dead_km + V_vn_gtm_ost_texn_km
# Остатки нефти на ВПУ на конец месяца, всего
    V_vn_gtm_ost_vpu_km = V_vn_gtm_ost_np_km + V_vn_gtm_ost_tov_km + V_vn_gtm_ost_texn_km
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор»)
    V_vn_gtm_path_km = V_vn_gtm_ost_nm + Q_vn_gtm_total - V_vn_gtm_lost - V_vn_gtm_ost_vpu_km - G_vn_gtm_release - G_vn_gtm_own - F_vn_gtm_total
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_vn_gtm_ost_km = V_vn_gtm_ost_vpu_km + V_vn_gtm_path_km
# Изменение остатков нефти (газового конденсата) собственных, всего
    delta_V_vn_gtm_ost = V_vn_gtm_ost_km - V_vn_gtm_ost_nm
#
    V_vn_gtm_check = (V_vn_gtm_ost_nm + Q_vn_gtm_total) - (V_vn_gtm_lost + G_vn_gtm_own + G_vn_gtm_release + F_vn_gtm_total + V_vn_gtm_ost_km)
    if V_vn_gtm_check != 0 or abs(V_tstn_vn - V_vn_gtm_path_nm) <=80:
        _status = 2
        _message = "Проверка не пройдена"
    else:
        _status = 1
        _message = "Проверка пройдена"
    return{
        "V_vn_gtm_ost_app_km":{"value": V_vn_gtm_ost_app_km, "status": _status, "message": _message},
        "V_vn_gtm_ost_tech_nm":{"value": V_vn_gtm_ost_texn_nm, "status": _status, "message": _message},
        "V_vn_gtm_ost_rvs_nm":{"value": V_vn_gtm_ost_rvs_nm, "status": _status, "message": _message},
        "V_vn_gtm_path_nm":{"value": V_vn_gtm_path_nm, "status": _status, "message": _message},
        "V_vn_gtm_ost_vpy_nm":{"value": V_vn_gtm_ost_vpy_nm, "status": _status, "message": _message},
        "V_vn_gtm_ost_nm":{"value": V_vn_gtm_ost_nm, "status": _status, "message": _message},
        "Q_vn_gtm_total":{"value": Q_vn_gtm_total, "status": _status, "message": _message},
        "Q_vn_gtm_oil":{"value": Q_vn_gtm_oil, "status": _status, "message": _message},
        "F_vn_gtm_total":{"value": F_vn_gtm_total, "status": _status, "message": _message},
        "V_vn_gtm_lost_oil":{"value": V_vn_gtm_lost_oil, "status": _status, "message": _message},
        "V_vn_gtm_lost_transport":{"value": V_vn_gtm_lost_transport, "status": _status, "message": _message},
        "V_vn_gtm_lost":{"value": V_vn_gtm_lost, "status": _status, "message": _message},
        "G_vn_gtm_own":{"value": G_vn_gtm_own, "status": _status, "message": _message},
        "G_vn_gtm_release_suzun":{"value": G_vn_gtm_release_suzun, "status": _status, "message": _message},
        "G_vn_gtm_release":{"value": G_vn_gtm_release, "status": _status, "message": _message},
        "V_vn_gtm_ost_np_km":{"value": V_vn_gtm_ost_np_km, "status": _status, "message": _message},
        "V_vn_gtm_ost_tech_km":{"value": V_vn_gtm_ost_texn_km, "status": _status, "message": _message},
        "V_vn_gtm_ost_dead_km":{"value": V_vn_gtm_ost_dead_km, "status": _status, "message": _message},
        "V_vn_gtm_ost_rvs_clean_km":{"value": V_vn_gtm_ost_rvs_clean_km, "status": _status, "message": _message},
        "V_vn_gtm_ost_tov_km":{"value": V_vn_gtm_ost_tov_km, "status": _status, "message": _message},
        "V_vn_gtm_ost_rvs_km":{"value": V_vn_gtm_ost_rvs_km, "status": _status, "message": _message},
        "V_vn_gtm_ost_vpu_km":{"value": V_vn_gtm_ost_vpu_km, "status": _status, "message": _message},
        "V_vn_gtm_path_km":{"value": V_vn_gtm_path_km, "status": _status, "message": _message},
        "V_vn_gtm_ost_km":{"value": V_vn_gtm_ost_km, "status": _status, "message": _message},
        "delta_V_vn_gtm_ost":{"value": delta_V_vn_gtm_ost, "status": _status, "message": _message},
        "V_vn_gtm_check":{"value": V_vn_gtm_check, "status": _status, "message": _message}
    }

def planned_balance_for_bp_suzun_gtm_calc(
        V_suzun_slu_0, V_suzun_vslu_0, V_suzun_gtm_ost_cps_nm, V_suzun_gtm_ost_np_nm, V_suzun_gtm_ost_app_nm, V_suzun_0, V_tstn_suzun_vankor_0, V_tstn_suzun_vslu_0,
        Q_suzun_month, Q_vslu_month, Q_suzun_gtm_condensate, K_suzun_prod, G_buying_oil_month, G_suzun_gtm_fuel, G_per_month, F_suzun_sum, F_suzun_vslu_sum,
        F_suzun_vankor_sum, K_suzun, K_vankor, V_suzun_gtm_ost_dead_nm, V_suzun_gtm_ost_tov_nm, V_suzun_slu, V_suzun_vslu,
        G_suzun_gtm_release_rn_drillig, V_suzun_gtm_ost_rvs_clean_nm, V_tstn_suzun_vankor, V_tstn_suzun, V_tstn_suzun_vslu
):
    V_suzun_gtm_ost_upn_nm = V_suzun_slu_0 + V_suzun_vslu_0
# Технологические остатки нефти в резервуарах СПУ на начало месяца отчетного периода
    V_suzun_gtm_ost_texn_nm = V_suzun_gtm_ost_upn_nm + V_suzun_gtm_ost_cps_nm
    V_suzun_gtm_ost_rvs = V_suzun_gtm_ost_dead_nm + V_suzun_gtm_ost_texn_nm
# Остатки нефти (газового конденсата) на СПУ
    V_suzun_gtm_ost_spy_nm = V_suzun_gtm_ost_np_nm + V_suzun_gtm_ost_app_nm + V_suzun_gtm_ost_texn_nm
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор») на начало месяца отчетного периода
    V_suzun_gtm_path_nm = V_suzun_0 + V_tstn_suzun_vankor_0 + V_tstn_suzun_vslu_0
# Остатки нефти (газового конденсата) АО «Сузун», всего
    V_suzun_gtm_ost_nm = V_suzun_gtm_ost_spy_nm + V_suzun_gtm_path_nm
# Добыча нефти Сузунского ЛУ
    Q_suzun_gtm_slu = Q_suzun_month
# Добыча нефти Восточно-Сузунского ЛУ
    Q_suzun_gtm_vslu = Q_vslu_month
# Добыча нефти (газового конденсата) АО «Сузун», всего
    Q_suzun_gtm_total = Q_suzun_gtm_slu + Q_suzun_gtm_vslu + Q_suzun_gtm_condensate
# Технологические потери нефти при добыче и подготовке
    V_suzun_gtm_lost_oil = round(Q_suzun_gtm_slu * (K_suzun_prod/100))
# Расход нефти (газового конденсата) на переработку на малогабаритных установках переработки нефти (МУПН)
    G_suzun_gtm_mupn = G_per_month
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_suzun_gtm_own = G_suzun_gtm_fuel + G_suzun_gtm_mupn
# Приобретение нефти у сторонних организаций (АО «Ванкорнефть»)
    G_suzun_gtm_buy = G_buying_oil_month
# Сдача нефти АО «Сузун» (Сузунский ЛУ)____Добавить после автобаланса
    F_suzun_gtm_slu = F_suzun_sum
# Сдача нефти АО «Сузун» (Восточно-Сузунский ЛУ)____Добавить после автобаланса
    F_suzun_gtm_vslu = F_suzun_vslu_sum
# Сдача нефти АО «Сузун» (АО «Ванкорнефть»)____Добавить после автобаланса
    F_suzun_gtm_vankor = F_suzun_vankor_sum
# Сдача нефти (газового конденсата) АО «Сузун», всего
    F_suzun_gtm_total = F_suzun_gtm_slu + F_suzun_gtm_vslu + F_suzun_gtm_vankor
# Технологические потери нефти (газового конденсата) при транспортировке (Сузунский ЛУ)
    V_suzun_gtm_lost_slu = round(F_suzun_gtm_slu * (K_suzun/100))
# Технологические потери нефти (газового конденсата) при транспортировке (Восточно-Сузунский ЛУ)
    V_suzun_gtm_lost_vslu = round(F_suzun_gtm_vslu * (K_suzun/100))
# Технологические потери нефти (газового конденсата) при транспортировке (Восточно-Сузунский ЛУ)
    V_suzun_gtm_lost_vankor = round(F_suzun_gtm_vankor * (K_vankor/100))
# Технологические потери нефти (газового конденсата), всего
    V_suzun_gtm_lost = V_suzun_gtm_lost_oil + V_suzun_gtm_lost_slu + V_suzun_gtm_lost_vslu + V_suzun_gtm_lost_vankor
    G_suzun_gtm_release = G_suzun_gtm_release_rn_drillig
# Остатки нефти на СПУ в нефтепроводах на конец месяца отчетного периода
    V_suzun_gtm_ost_np_km = V_suzun_gtm_ost_np_nm
# Остатки нефти в аппаратах СПУ на конец месяца отчетного периода
    V_suzun_gtm_ost_app_km = V_suzun_gtm_ost_app_nm
# Мертвые остатки нефти в резервуарах СПУ на конец месяца отчетного
    V_suzun_gtm_ost_dead_km = V_suzun_gtm_ost_dead_nm
# Товарные остатки нефти на конец месяца отчетного периода
    V_suzun_gtm_ost_cps_km = V_suzun_gtm_ost_cps_nm
    V_suzun_gtm_ost_rvs_clean_km = V_suzun_gtm_ost_rvs_clean_nm

    V_suzun_gtm_ost_tov_km = V_suzun_gtm_ost_tov_nm
# Технологические остатки нефти в резервуарах УПН ЦППН №2 на конец месяца отчетного периода
    V_suzun_gtm_ost_upn_km = V_suzun_slu + V_suzun_vslu
# Технологические остатки нефти СПУ на конец месяца отчетного периода
    V_suzun_gtm_ost_texn_km = V_suzun_gtm_ost_upn_km + V_suzun_gtm_ost_cps_km
# Остатки нефти в резервуарах СПУ на конец месяца отчетного периода
    V_suzun_gtm_ost_spu_km = V_suzun_gtm_ost_np_km + V_suzun_gtm_ost_app_km + V_suzun_gtm_ost_texn_km
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор»)
    V_suzun_gtm_path_km = V_suzun_gtm_ost_nm + Q_suzun_gtm_total - V_suzun_gtm_lost - V_suzun_gtm_ost_spu_km - G_suzun_gtm_release - G_suzun_gtm_own - F_suzun_gtm_total + G_suzun_gtm_buy
# Остатки нефти (газового конденсата) на конец месяца отчетного периода, всего
    V_suzun_gtm_ost_km = V_suzun_gtm_ost_spu_km + V_suzun_gtm_path_km
    
    delta_V_suzun_gtm_ost = V_suzun_gtm_ost_km - V_suzun_gtm_ost_nm
# Проверка
    V_suzun_gtm_check = (V_suzun_gtm_ost_nm + Q_suzun_gtm_total + G_suzun_gtm_buy) - (V_suzun_gtm_lost + G_suzun_gtm_own + G_suzun_gtm_release + F_suzun_gtm_total + V_suzun_gtm_ost_km)
    if V_suzun_gtm_check != 0:
        _status = 2
        _message = "Проверка не пройдена"
        V_suzun_balance_total = None
    else:
        V_suzun_balance_total = V_tstn_suzun_vankor + V_tstn_suzun + V_tstn_suzun_vslu
        if abs(V_suzun_balance_total - V_suzun_gtm_path_km) > 20:
            _status = 2
            _message = "Проверка не пройдена"
        else:
            _status = 1
            _message = "Проверка пройдена"

    return{
        "V_suzun_gtm_ost_tech_nm":{"value": V_suzun_gtm_ost_texn_nm, "status": _status, "message": _message},
        "V_suzun_gtm_ost_upn_nm":{"value": V_suzun_gtm_ost_upn_nm, "status": _status, "message": _message},
        "V_suzun_gtm_ost_rvs_nm":{"value": V_suzun_gtm_ost_rvs, "status": _status, "message": _message},
        "V_suzun_gtm_ost_spy_nm":{"value": V_suzun_gtm_ost_spy_nm, "status": _status, "message": _message},
        "V_suzun_gtm_path_nm":{"value": V_suzun_gtm_path_nm, "status": _status, "message": _message},
        "V_suzun_gtm_ost_nm":{"value": V_suzun_gtm_ost_nm, "status": _status, "message": _message},
        "Q_suzun_gtm_slu":{"value": Q_suzun_gtm_slu, "status": _status, "message": _message},
        "Q_suzun_gtm_vslu":{"value": Q_suzun_gtm_vslu, "status": _status, "message": _message},
        "Q_suzun_gtm_total":{"value": Q_suzun_gtm_total, "status": _status, "message": _message},
        "V_suzun_gtm_lost_oil":{"value": V_suzun_gtm_lost_oil, "status": _status, "message": _message},
        "G_suzun_gtm_mupn":{"value": G_suzun_gtm_mupn, "status": _status, "message": _message},
        "G_suzun_gtm_own":{"value": G_suzun_gtm_own, "status": _status, "message": _message},
        "G_suzun_gtm_buy":{"value": G_suzun_gtm_buy, "status": _status, "message": _message},
        "F_suzun_gtm_slu":{"value": F_suzun_gtm_slu, "status": _status, "message": _message},
        "F_suzun_gtm_vslu":{"value": F_suzun_gtm_vslu, "status": _status, "message": _message},
        "F_suzun_gtm_vankor":{"value": F_suzun_gtm_vankor, "status": _status, "message": _message},
        "F_suzun_gtm_total":{"value": F_suzun_gtm_total, "status": _status, "message": _message},
        "V_suzun_gtm_lost_slu":{"value": V_suzun_gtm_lost_slu, "status": _status, "message": _message},
        "V_suzun_gtm_lost_vslu":{"value": V_suzun_gtm_lost_vslu, "status": _status, "message": _message},
        "V_suzun_gtm_lost_vankor":{"value": V_suzun_gtm_lost_vankor, "status": _status, "message": _message},
        "V_suzun_gtm_lost":{"value": V_suzun_gtm_lost, "status": _status, "message": _message},
        "V_suzun_gtm_ost_np_km":{"value": V_suzun_gtm_ost_np_km, "status": _status, "message": _message},
        "V_suzun_gtm_ost_app_km":{"value": V_suzun_gtm_ost_app_km, "status": _status, "message": _message},
        "V_suzun_gtm_ost_dead_km":{"value": V_suzun_gtm_ost_dead_km, "status": _status, "message": _message},
        "V_suzun_gtm_ost_tov_km":{"value": V_suzun_gtm_ost_tov_km, "status": _status, "message": _message},
        "V_suzun_gtm_ost_upn_km":{"value": V_suzun_gtm_ost_upn_km, "status": _status, "message": _message},
        "V_suzun_gtm_ost_rvs_clean_km":{"value": V_suzun_gtm_ost_rvs_clean_km, "status": _status, "message": _message},
        "V_suzun_gtm_ost_spu_km":{"value": V_suzun_gtm_ost_spu_km, "status": _status, "message": _message},
        "V_suzun_gtm_path_km":{"value": V_suzun_gtm_path_km, "status": _status, "message": _message},
        "V_suzun_gtm_ost_km":{"value": V_suzun_gtm_ost_km, "status": _status, "message": _message},
        "delta_V_suzun_gtm_ost":{"value": delta_V_suzun_gtm_ost, "status": _status, "message": _message},
        "V_suzun_gtm_ost_tech_km":{"value": V_suzun_gtm_ost_texn_km, "status": _status, "message": _message},
        "V_suzun_gtm_ost_cps_km":{"value": V_suzun_gtm_ost_cps_km, "status": _status, "message": _message},
        "G_suzun_gtm_release":{"value": G_suzun_gtm_release, "status": _status, "message": _message},
        "V_suzun_gtm_check":{"value": V_suzun_gtm_check, "status": _status, "message": _message},
        "V_suzun_balance_total":{"value": V_suzun_balance_total, "status": _status, "message": _message},
    }
# _____________Формирование планового баланса добычи-сдачи нефти по ООО «Восток Ойл» (Бизнес-план):_____________
def planned_balance_for_bp_vo_gtm_calc(
        V_ichem_0, V_vo_gtm_ost_dead_nm, V_vo_gtm_ost_tech_nm, V_vo_gtm_ost_tov_nm, V_tstn_vo_0, V_vo_gtm_ost_np_nm, V_vo_gtm_ost_app_nm, Q_vo_month,
        Q_vo_gtm_condensate, F_vo_sum, K_vo_prod, K_vo_transp, V_vo_gtm_lost_condensate, G_vo_gtm_fuel, G_vo_gtm_fill, V_ichem, G_vo_gtm_release, V_tstn_vo

):
# Остатки нефти на УПН Лодочное на начало месяца отчетного периода
    V_vo_gtm_ost_upn_lodochny_nm = V_ichem_0
# Остатки нефти в резервуарах ВПУ на начало месяца отчетного периода
    V_vo_gtm_ost_rvs_nm = V_vo_gtm_ost_dead_nm + V_vo_gtm_ost_tech_nm + V_vo_gtm_ost_upn_lodochny_nm + V_vo_gtm_ost_tov_nm
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор») на начало месяца отчетного периода
    V_vo_gtm_path_nm = V_tstn_vo_0
# Остатки нефти (газового конденсата) на ВПУ
    V_vo_gtm_ost_vpy_nm = V_vo_gtm_ost_np_nm + V_vo_gtm_ost_app_nm + V_vo_gtm_ost_rvs_nm
# Остатки нефти (газового конденсата) ООО «Восток Ойл», всего
    V_vo_gtm_ost_nm = V_vo_gtm_ost_vpy_nm + V_vo_gtm_path_nm
# Добыча нефти ООО «Восток Ойл»
    Q_vo_gtm_oil = Q_vo_month
# Добыча нефти (газового конденсата) ООО «Восток Ойл», всего
    Q_vo_gtm_total = Q_vo_gtm_oil + Q_vo_gtm_condensate
# Сдача нефти (газового конденсата) ООО «Восток Ойл», всего
    F_vo_gtm_total = F_vo_sum
# Технологические потери нефти при добыче и подготовке
    V_vo_gtm_lost_oil = round(Q_vo_gtm_oil * (K_vo_prod/100))
# Технологические потери нефти (газового конденсата) при транспортировке
    V_vo_gtm_lost_transport = round(F_vo_gtm_total * (K_vo_transp/100))
# Технологические потери нефти (газового конденсата), всего
    V_vo_gtm_lost = V_vo_gtm_lost_oil + V_vo_gtm_lost_condensate + V_vo_gtm_lost_transport
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_vo_gtm_own = G_vo_gtm_fuel + G_vo_gtm_fill
# Остатки нефти на ВПУ в нефтепроводах на конец месяца отчетного периода
    V_vo_gtm_ost_np_km = V_vo_gtm_ost_np_nm
# Остатки нефти в аппаратах ВПУ на конец месяца отчетного периода
    V_vo_gtm_ost_app_km = V_vo_gtm_ost_app_nm
# Мертвые остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_vo_gtm_ost_dead_km = V_vo_gtm_ost_dead_nm
# Технологические остатки нефти на ВПУ на конец месяца отчетного периода
    V_vo_gtm_ost_tech_km = V_vo_gtm_ost_tech_nm
# Товарные остатки нефти на ВПУ на конец месяца отчетного периода
    V_vo_gtm_ost_tov_km = V_vo_gtm_ost_tov_nm
# Остатки нефти ООО «Восток Ойл» на УПН Лодочное на конец месяца отчетного периода
    V_vo_gtm_ost_upn_lodochny_km = V_ichem
# Остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_vo_gtm_ost_rvs_km = V_vo_gtm_ost_dead_km + V_vo_gtm_ost_tech_km + V_vo_gtm_ost_upn_lodochny_km + V_vo_gtm_ost_tov_km
# Остатки нефти на ВПУ на конец месяца отчетного периода
    V_vo_gtm_ost_vpy_km = V_vo_gtm_ost_np_km + V_vo_gtm_ost_app_km + V_vo_gtm_ost_rvs_km
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор»)
    V_vo_gtm_path_km = V_vo_gtm_ost_nm + Q_vo_gtm_total - V_vo_gtm_lost - V_vo_gtm_ost_vpy_km - G_vo_gtm_release - G_vo_gtm_own - F_vo_gtm_total
# Остатки нефти (газового конденсата) на конец месяца отчетного периода, всего
    V_vo_gtm_ost_km = V_vo_gtm_ost_vpy_km + V_vo_gtm_path_km
# Изменение остатков нефти (газового конденсата) собственных, всего
    delta_V_vo_gtm_ost = V_vo_gtm_ost_km - V_vo_gtm_ost_nm
# Выполнение процедуры проверки
    V_vo_gtm_check = (V_vo_gtm_ost_nm + Q_vo_gtm_total) - (V_vo_gtm_lost + G_vo_gtm_own + G_vo_gtm_release + F_vo_gtm_total + V_vo_gtm_ost_km)
    if V_vo_gtm_check != 0 or abs(V_tstn_vo - V_vo_gtm_path_km) > 40:
        _status = 2
        _message = "Проверка не пройдена"
    else:
        _status = 1
        _message = "Проверка не пройдена"

    return{
        "V_vo_gtm_ost_upn_lodochny_nm":{"value": V_vo_gtm_ost_upn_lodochny_nm, "status": _status, "message": _message},
        "V_vo_gtm_ost_rvs_nm":{"value": V_vo_gtm_ost_rvs_nm, "status": _status, "message": _message},
        "V_vo_gtm_path_nm":{"value": V_vo_gtm_path_nm, "status": _status, "message": _message},
        "V_vo_gtm_ost_vpy_nm":{"value": V_vo_gtm_ost_vpy_nm, "status": _status, "message": _message},
        "V_vo_gtm_ost_nm":{"value": V_vo_gtm_ost_nm, "status": _status, "message": _message},
        "Q_vo_gtm_oil":{"value": Q_vo_gtm_oil, "status": _status, "message": _message},
        "Q_vo_gtm_total":{"value": Q_vo_gtm_total, "status": _status, "message": _message},
        "F_vo_gtm_total":{"value": F_vo_gtm_total, "status": _status, "message": _message},
        "V_vo_gtm_lost_oil":{"value": V_vo_gtm_lost_oil, "status": _status, "message": _message},
        "V_vo_gtm_lost_transport":{"value": V_vo_gtm_lost_transport, "status": _status, "message": _message},
        "V_vo_gtm_lost":{"value": V_vo_gtm_lost, "status": _status, "message": _message},
        "G_vo_gtm_own":{"value": G_vo_gtm_own, "status": _status, "message": _message},
        "V_vo_gtm_ost_np_km":{"value": V_vo_gtm_ost_np_km, "status": _status, "message": _message},
        "V_vo_gtm_ost_app_km":{"value": V_vo_gtm_ost_app_km, "status": _status, "message": _message},
        "V_vo_gtm_ost_dead_km":{"value": V_vo_gtm_ost_dead_km, "status": _status, "message": _message},
        "V_vo_gtm_ost_tech_km":{"value": V_vo_gtm_ost_tech_km, "status": _status, "message": _message},
        "V_vo_gtm_ost_tov_km":{"value": V_vo_gtm_ost_tov_km, "status": _status, "message": _message},
        "V_vo_gtm_ost_upn_lodochny_km":{"value": V_vo_gtm_ost_upn_lodochny_km, "status": _status, "message": _message},
        "V_vo_gtm_ost_rvs_km":{"value": V_vo_gtm_ost_rvs_km, "status": _status, "message": _message},
        "V_vo_gtm_ost_vpy_km":{"value": V_vo_gtm_ost_vpy_km, "status": _status, "message": _message},
        "V_vo_gtm_path_km":{"value": V_vo_gtm_path_km, "status": _status, "message": _message},
        "V_vo_gtm_ost_km":{"value": V_vo_gtm_ost_km, "status": _status, "message": _message},
        "delta_V_vo_gtm_ost":{"value": delta_V_vo_gtm_ost, "status": _status, "message": _message},
        "V_vo_gtm_check":{"value": V_vo_gtm_check, "status": _status, "message": _message}
    }

# _____________Формирование планового баланса добычи-сдачи нефти по ООО «Тагульское» Лодочное месторождение (Бизнес-план):_____________
def planned_balance_for_bp_lodochny_gtm_calc(
        V_lodochny_0, V_lodochny_gtm_ost_upn_ichem_nm, V_lodochny_gtm_ost_upsv_yu_nm, V_tstn_lodochny_0, V_lodochny_gtm_ost_np_nm, V_lodochny_gtm_ost_app_nm,
        Q_lodochny_month, Q_lodochny_gtm_condensate, F_tagul_lpu_sum, K_lodochny_prod, K_lodochny_transp, V_lodochny_gtm_ost_dead_nm, V_lodochny_gtm_ost_tov_nm,
        V_lodochny_gtm_ost_rvs_clean_nm, V_lodochny, G_lodochny_gtm_release, G_lodochny_gtm_own, V_tstn_lodochny
):
# Остатки нефти на УПН Лодочное на начало месяца отчетного периода
    V_lodochny_gtm_ost_upn_lodochny_nm = V_lodochny_0
# Остатки нефти в резервуарах ЛПУ на начало месяца отчетного периода
    V_lodochny_gtm_ost_rvs_nm = V_lodochny_gtm_ost_upn_lodochny_nm + V_lodochny_gtm_ost_upn_ichem_nm + V_lodochny_gtm_ost_upsv_yu_nm
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор») на начало месяца отчетного периода
    V_lodochny_gtm_path_nm = V_tstn_lodochny_0
# Остатки нефти (газового конденсата) ООО «Тагульское» Лодочное месторождение, всего
    V_lodochny_gtm_ost_nm = V_lodochny_gtm_ost_np_nm + V_lodochny_gtm_ost_app_nm + V_lodochny_gtm_ost_rvs_nm + V_lodochny_gtm_path_nm
# Добыча нефти ООО «Тагульское» Лодочное месторождение
    Q_lodochny_gtm_oil = Q_lodochny_month
# Добыча нефти (газового конденсата) ООО «Тагульское» Лодочное месторождение, всего
    Q_lodochny_gtm_total = Q_lodochny_gtm_oil + Q_lodochny_gtm_condensate
# Сдача нефти (газового конденсата) ООО «Тагульское» Лодочное месторождение, всего
    F_lodochny_gtm_total = F_tagul_lpu_sum
# Технологические потери нефти при добыче и подготовке
    V_lodochny_gtm_lost_oil = round(Q_lodochny_gtm_oil * (K_lodochny_prod/100))
# Технологические потери нефти (газового конденсата) при транспортировке
    V_lodochny_gtm_lost_transport = round(F_lodochny_gtm_total * (K_lodochny_transp/100))
# Технологические потери нефти (газового конденсата), всего
    V_lodochny_gtm_lost = V_lodochny_gtm_lost_oil + V_lodochny_gtm_lost_transport
# Остатки нефти на ЛПУ в нефтепроводах на конец месяца отчетного периода
    V_lodochny_gtm_ost_np_km = V_lodochny_gtm_ost_np_nm
# Остатки нефти в аппаратах ЛПУ на конец месяца отчетного периода
    V_lodochny_gtm_ost_app_km = V_lodochny_gtm_ost_app_nm
# Мертвые остатки нефти на ЛПУ на конец месяца отчетного периода
    V_lodochny_gtm_ost_dead_km = V_lodochny_gtm_ost_dead_nm
# Технологические остатки нефти Ичемминского м/р на УПН Лодочного на конец месяца отчетного периода
    V_lodochny_gtm_ost_upn_ichem_km = V_lodochny_gtm_ost_upn_ichem_nm
# Технологические остатки нефти на УПСВ-Юг на конец месяца отчетного периода
    V_lodochny_gtm_ost_upsv_yu_km = V_lodochny_gtm_ost_upsv_yu_nm
# Товарные остатки нефти на конец месяца отчетного периода
    V_lodochny_gtm_ost_tov_km = V_lodochny_gtm_ost_tov_nm
# Остатки нефти в РВС очистных сооружений на конец месяца отчетного периода
    V_lodochny_gtm_ost_rvs_clean_km = V_lodochny_gtm_ost_rvs_clean_nm
# Остатки нефти ООО «Тагульское» на УПН Лодочное на конец месяца отчетного периода
    V_lodochny_gtm_ost_upn_lodochny_km = V_lodochny
# Технологические остатки нефти ООО «Тагульское» (Лодочное месторождение) на конец месяца отчетного периода, всего
    V_lodochny_gtm_ost_tech_km = V_lodochny_gtm_ost_upn_lodochny_km + V_lodochny_gtm_ost_upn_ichem_km + V_lodochny_gtm_ost_upsv_yu_km
# Остатки нефти в резервуарах ЛПУ на конец месяца отчетного периода
    V_lodochny_gtm_ost_rvs_km = V_lodochny_gtm_ost_dead_km + V_lodochny_gtm_ost_tech_km
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор»)
    V_lodochny_gtm_path_km = V_lodochny_gtm_ost_nm + Q_lodochny_gtm_total - V_lodochny_gtm_lost - V_lodochny_gtm_ost_np_km - V_lodochny_gtm_ost_app_km - V_lodochny_gtm_ost_rvs_km - G_lodochny_gtm_release - G_lodochny_gtm_own - F_lodochny_gtm_total
# Остатки нефти (газового конденсата) на конец месяца отчетного периода, всего
    V_lodochny_gtm_ost_km = V_lodochny_gtm_ost_np_km + V_lodochny_gtm_ost_app_km + V_lodochny_gtm_ost_rvs_km + V_lodochny_gtm_path_km
# Изменение остатков нефти (газового конденсата) собственных, всего
    delta_V_lodochny_gtm_ost = V_lodochny_gtm_ost_km - V_lodochny_gtm_ost_nm
# Выполнение процедуры проверки
    V_lodochny_gtm_check = (V_lodochny_gtm_ost_nm + Q_lodochny_gtm_total) - (V_lodochny_gtm_lost + F_lodochny_gtm_total + V_lodochny_gtm_ost_km)
    if V_lodochny_gtm_check != 0 or abs(V_tstn_lodochny - V_lodochny_gtm_path_km) > 5:
        _status = 2
        _message = "Проверка не пройдена"
    else:
        _status = 1
        _message = "Проверка пройдена"
    return{
        "V_lodochny_gtm_ost_upn_lodochny_nm":{"value": V_lodochny_gtm_ost_upn_lodochny_nm, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_rvs_nm":{"value": V_lodochny_gtm_ost_rvs_nm, "status": _status, "message": _message},
        "V_lodochny_gtm_path_nm":{"value": V_lodochny_gtm_path_nm, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_nm":{"value": V_lodochny_gtm_ost_nm, "status": _status, "message": _message},
        "Q_lodochny_gtm_oil":{"value": Q_lodochny_gtm_oil, "status": _status, "message": _message},
        "Q_lodochny_gtm_total":{"value": Q_lodochny_gtm_total, "status": _status, "message": _message},
        "F_lodochny_gtm_total":{"value": F_lodochny_gtm_total, "status": _status, "message": _message},
        "V_lodochny_gtm_lost_oil":{"value": V_lodochny_gtm_lost_oil, "status": _status, "message": _message},
        "V_lodochny_gtm_lost_transport":{"value": V_lodochny_gtm_lost_transport, "status": _status, "message": _message},
        "V_lodochny_gtm_lost":{"value": V_lodochny_gtm_lost, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_np_km":{"value": V_lodochny_gtm_ost_np_km, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_app_km":{"value": V_lodochny_gtm_ost_app_km, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_dead_km":{"value": V_lodochny_gtm_ost_dead_km, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_upn_ichem_km":{"value": V_lodochny_gtm_ost_upn_ichem_km, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_upsv_yu_km":{"value": V_lodochny_gtm_ost_upsv_yu_km, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_tov_km":{"value": V_lodochny_gtm_ost_tov_km, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_rvs_clean_km":{"value": V_lodochny_gtm_ost_rvs_clean_km, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_upn_lodochny_km":{"value": V_lodochny_gtm_ost_upn_lodochny_km, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_tech_km":{"value": V_lodochny_gtm_ost_tech_km, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_rvs_km":{"value": V_lodochny_gtm_ost_rvs_km, "status": _status, "message": _message},
        "V_lodochny_gtm_path_km":{"value": V_lodochny_gtm_path_km, "status": _status, "message": _message},
        "V_lodochny_gtm_ost_km":{"value": V_lodochny_gtm_ost_km, "status": _status, "message": _message},
        "delta_V_lodochny_gtm_ost":{"value": delta_V_lodochny_gtm_ost, "status": _status, "message": _message},
        "V_lodochny_gtm_check":{"value": V_lodochny_gtm_check, "status": _status, "message": _message},
    }
# _____________Формирование планового баланса добычи-сдачи нефти по ООО «Тагульское» Тагульское месторождение (ГТМ):_____________
def planned_balance_for_bp_tagul_gtm_calc(
        V_tagul_gtm_ost_dead_nm, V_tagul_gtm_ost_tech_nm, V_tagul_gtm_ost_rvs_clean_nm, V_tagul_gtm_ost_tov_nm, V_tagul_gtm_ost_np_nm, V_tagul_gtm_ost_app_nm,
        V_tstn_tagul_0, Q_tagul_month, Q_tagul_gtm_condensate, F_tagul_tpu_sum, K_tagul_prod, K_tagul, G_tagul_gtm_fuel, G_tagul_gtm_release_rn_drillig,
        G_tagul_gtm_release_rr, V_tagul_gtm_ost_np_km, V_tagul_gtm_ost_app_km, V_tstn_tagul
):
# Остатки нефти в резервуарах ТПУ на начало месяца отчетного периода
    V_tagul_gtm_ost_rvs_nm = V_tagul_gtm_ost_dead_nm + V_tagul_gtm_ost_tech_nm + V_tagul_gtm_ost_rvs_clean_nm + V_tagul_gtm_ost_tov_nm
# Остатки нефти (газового конденсата) на ТПУ
    V_tagul_gtm_ost_tpu_nm = V_tagul_gtm_ost_np_nm + V_tagul_gtm_ost_app_nm + V_tagul_gtm_ost_rvs_nm
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор») на начало месяца отчетного периода
    V_tagul_gtm_path_nm = V_tstn_tagul_0
# Остатки нефти (газового конденсата) ООО «Тагульское» Тагульское месторождение, всего
    V_tagul_gtm_ost_nm = V_tagul_gtm_ost_tpu_nm + V_tagul_gtm_ost_dead_nm + V_tagul_gtm_path_nm
# Добыча нефти (ООО «Тагульское» Тагульское месторождения
    Q_tagul_gtm_oil = Q_tagul_month
# Добыча нефти (газового конденсата) ООО «Тагульское» Тагульское месторождения, всего
    Q_tagul_gtm_total = Q_tagul_gtm_oil + Q_tagul_gtm_condensate
# Сдача нефти (газового конденсата) ООО «Тагульское» Тагульское месторождение
    F_tagul_gtm_total = F_tagul_tpu_sum
# Технологические потери нефти при добыче и подготовке
    V_tagul_gtm_lost_oil = round(Q_tagul_gtm_total * (K_tagul_prod/100))
# Технологические потери нефти (газового конденсата) при транспортировке
    V_tagul_gtm_lost_transport = round(F_tagul_gtm_total * (K_tagul/100))
# Технологические потери нефти (газового конденсата), всего
    V_tagul_gtm_lost = V_tagul_gtm_lost_oil + V_tagul_gtm_lost_transport
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_tagul_gtm_own = G_tagul_gtm_fuel
# Отпуск нефти (газового конденсата) ООО «Тагульское» Тагульское месторождение, всего
    G_tagul_gtm_release = G_tagul_gtm_release_rn_drillig + G_tagul_gtm_release_rr
# Технологические остатки нефти в резервуарах ТПУ на конец месяца
    V_tagul_gtm_ost_tech_km = V_tagul_gtm_ost_tech_nm
# Мертвые остатки нефти в резервуарах ТПУ на конец месяца отчетного периода
    V_tagul_gtm_ost_dead_km = V_tagul_gtm_ost_dead_nm
# Технологические остатки нефти в резервуарах ТПУ на конец месяца отчетного периода_____________________________________________________
    V_tagul_gtm_ost_rvs_clean_km = V_tagul_gtm_ost_rvs_clean_nm
# Товарные остатки нефти на конец месяца отчетного периода
    V_tagul_gtm_ost_tov_km = V_tagul_gtm_ost_tov_nm
# Остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_tagul_gtm_ost_rvs_km = V_tagul_gtm_ost_dead_km + V_tagul_gtm_ost_tech_km + V_tagul_gtm_ost_rvs_clean_km + V_tagul_gtm_ost_tov_km
# Остатки нефти на ТПУ на конец месяца, всего
    V_tagul_gtm_ost_tpu_km = V_tagul_gtm_ost_np_km + V_tagul_gtm_ost_app_km + V_tagul_gtm_ost_rvs_km
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор»)
    V_tagul_gtm_path_km = V_tagul_gtm_ost_nm + Q_tagul_gtm_total - V_tagul_gtm_lost - V_tagul_gtm_ost_tpu_km - G_tagul_gtm_release - G_tagul_gtm_own - F_tagul_gtm_total
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_tagul_gtm_ost_km = V_tagul_gtm_ost_tpu_km + V_tagul_gtm_path_km
# Изменение остатков нефти (газового конденсата) собственных, всего
    delta_V_tagul_gtm_ost = V_tagul_gtm_ost_km - V_tagul_gtm_ost_nm
# Выполнение процедуры проверки
    V_tagul_gtm_check = (V_tagul_gtm_ost_nm + Q_tagul_gtm_total) - (V_tagul_gtm_lost + G_tagul_gtm_own + G_tagul_gtm_release + F_tagul_gtm_total + V_tagul_gtm_ost_km)
    if V_tagul_gtm_check != 0 or abs(V_tstn_tagul - V_tagul_gtm_path_km) > 5:
        _status = 2
        _message = "Проверка не пройдена"
    else:
        _status = 1
        _message = "Проверка пройдена"
    return{
        "V_tagul_gtm_ost_rvs_nm":{"value": V_tagul_gtm_ost_rvs_nm, "status": _status, "message": _message},
        "V_tagul_gtm_ost_tpu_nm":{"value": V_tagul_gtm_ost_tpu_nm, "status": _status, "message": _message},
        "V_tagul_gtm_path_nm":{"value": V_tagul_gtm_path_nm, "status": _status, "message": _message},
        "V_tagul_gtm_ost_nm":{"value": V_tagul_gtm_ost_nm, "status": _status, "message": _message},
        "Q_tagul_gtm_oil":{"value": Q_tagul_gtm_oil, "status": _status, "message": _message},
        "Q_tagul_gtm_total":{"value": Q_tagul_gtm_total, "status": _status, "message": _message},
        "F_tagul_gtm_total":{"value": F_tagul_gtm_total, "status": _status, "message": _message},
        "V_tagul_gtm_lost_oil":{"value": V_tagul_gtm_lost_oil, "status": _status, "message": _message},
        "V_tagul_gtm_lost_transport":{"value": V_tagul_gtm_lost_transport, "status": _status, "message": _message},
        "V_tagul_gtm_lost":{"value": V_tagul_gtm_lost, "status": _status, "message": _message},
        "G_tagul_gtm_own":{"value": G_tagul_gtm_own, "status": _status, "message": _message},
        "G_tagul_gtm_release":{"value": G_tagul_gtm_release, "status": _status, "message": _message},
        "V_tagul_gtm_ost_tech_km":{"value": V_tagul_gtm_ost_tech_km, "status": _status, "message": _message},
        "V_tagul_gtm_ost_dead_km":{"value": V_tagul_gtm_ost_dead_km, "status": _status, "message": _message},
        "V_tagul_gtm_ost_rvs_clean_km":{"value": V_tagul_gtm_ost_rvs_clean_km, "status": _status, "message": _message},
        "V_tagul_gtm_ost_tov_km":{"value": V_tagul_gtm_ost_tov_km, "status": _status, "message": _message},
        "V_tagul_gtm_ost_rvs_km":{"value": V_tagul_gtm_ost_rvs_km, "status": _status, "message": _message},
        "V_tagul_gtm_ost_tpu_km":{"value": V_tagul_gtm_ost_tpu_km, "status": _status, "message": _message},
        "V_tagul_gtm_path_km":{"value": V_tagul_gtm_path_km, "status": _status, "message": _message},
        "V_tagul_gtm_ost_km":{"value": V_tagul_gtm_ost_km, "status": _status, "message": _message},
        "V_tagul_gtm_check":{"value": V_tagul_gtm_check, "status": _status, "message": _message},
        "delta_V_tagul_gtm_ost":{"value": delta_V_tagul_gtm_ost, "status": _status, "message": _message},
    }


# ------------------------------------------------------------------
# Пересчёт F_bp_* при наличии node (остановка/ремонт).
# Получает текущие F_bp_* и текст node, корректирует значения.
# ------------------------------------------------------------------
def node_correction_calc(
    F_bp_vn, F_bp_suzun, F_bp_suzun_vankor, F_bp_suzun_vslu,
    F_bp_tagul, F_bp_tagul_lpu, F_bp_tagul_tpu,
    F_bp_skn, F_bp_vo, F_bp_tng, F_bp_kchng,
    node, t_ost_sikn_1209=0,
):
    parts = node.split()
    obj = parts[1] if len(parts) > 1 else ""

    K_work = None
    F_vn = None
    F_suzun = None
    F_suzun_vankor = None
    F_suzun_vslu = None
    F_tagul = None
    F_tagul_lpu = None
    F_tagul_tpu = None
    F_skn = None
    F_vo = None
    F_tng = None
    F_kchng = None
    F = None

    if obj == "СИКН-1209":
        K_work = (24 - t_ost_sikn_1209) / 24
        F_vn = F_bp_vn * K_work
        F_suzun = F_bp_suzun * K_work
        F_suzun_vankor = F_bp_suzun_vankor * K_work
        F_suzun_vslu = F_bp_suzun_vslu * K_work
        F_tagul = F_bp_tagul * K_work
        F_tagul_lpu = F_bp_tagul_lpu * K_work
        F_tagul_tpu = F_bp_tagul_tpu * K_work
        F_skn = F_bp_skn * K_work
        F_vo = F_bp_vo * K_work
        F_tng = F_bp_tng * K_work
        F_kchng = F_bp_kchng * K_work
        F = F_vn + F_suzun + F_suzun_vankor + F_suzun_vslu + F_tagul + F_tagul_lpu + F_tagul_tpu + F_skn + F_vo + F_tng + F_kchng

    elif obj in ("НПС-1", "НПС-2"):
        pass

    elif obj in ("НПС-1", "НПС-2") and obj in ("СИКН-1209"):
        pass

    return {
        "K_work": K_work,
        "F_vn": F_vn,
        "F_suzun": F_suzun,
        "F_suzun_vankor": F_suzun_vankor,
        "F_suzun_vslu": F_suzun_vslu,
        "F_tagul": F_tagul,
        "F_tagul_lpu": F_tagul_lpu,
        "F_tagul_tpu": F_tagul_tpu,
        "F_skn": F_skn,
        "F_vo": F_vo,
        "F_tng": F_tng,
        "F_kchng": F_kchng,
        "F": F,
    }
def adjusting_availability_oil_RP_CTN(
    t_ost_sikn_1209, V_knps, VN_knps_min,
    delta_VO_nps_1_max, delta_VO_gnps_max, delta_VO_nps_2_max,
    V_nps_1_prev, V_nps_2_prev,
    VA_nps_2_max, VA_nps_1_max, G_gnps_prev,
    day_type="adj", segment_length=0,
):
    delta_V_knps = None
    V_nps_1 = None
    V_nps_2 = None
    G_gnps = None

    if t_ost_sikn_1209 < 24:
        total_max = delta_VO_gnps_max + delta_VO_nps_1_max + delta_VO_nps_2_max
        delta_V_knps = V_knps - VN_knps_min

        if day_type == "adj":
            delta_V_nps_1 = delta_V_knps * (delta_VO_nps_1_max / total_max)
            if delta_V_nps_1 > delta_VO_nps_1_max:
                delta_V_nps_1 = delta_VO_nps_1_max
            V_nps_1 = V_nps_1_prev + delta_V_nps_1
            if V_nps_1 > VA_nps_1_max:
                V_nps_1 = VA_nps_1_max

            delta_V_nps_2 = delta_V_knps * (delta_VO_nps_2_max / total_max)
            if delta_V_nps_2 > delta_VO_nps_2_max:
                delta_V_nps_2 = delta_VO_nps_2_max
            V_nps_2 = V_nps_2_prev + delta_V_nps_2
            if V_nps_2 > VA_nps_2_max:
                V_nps_2 = VA_nps_2_max

            delta_V_gnps = delta_V_knps * (delta_VO_gnps_max / total_max)
            if delta_V_gnps > delta_VO_gnps_max:
                delta_V_gnps = delta_VO_gnps_max
            G_gnps = G_gnps_prev - delta_V_gnps
            if G_gnps < ((V_nps_1 - V_nps_1_prev) + (V_nps_2 - V_nps_2_prev)):
                G_gnps = (V_nps_1 - V_nps_1_prev) + (V_nps_2 - V_nps_2_prev)

        elif day_type == "between":
            # Дни между остановами: равномерный возврат к нормативу за segment_length дней
            G_gnps = (G_gnps + 8500)/segment_length

        elif day_type == "after":
            # Дни после последнего останова до конца месяца: равномерный возврат за segment_length дней
            V_nps_1 = V_nps_1_prev
            V_nps_2 = V_nps_2_prev
            G_gnps = G_gnps_prev

    return {
        "delta_V_knps": delta_V_knps,
        "V_nps_1": V_nps_1,
        "V_nps_2": V_nps_2,
        "G_gnps": G_gnps,
    }