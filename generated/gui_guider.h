/*
* Copyright 2025 NXP
* NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
* accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
* activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
* comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
* terms, then you may not retain, install, activate or otherwise use the software.
*/

#ifndef GUI_GUIDER_H
#define GUI_GUIDER_H
#ifdef __cplusplus
extern "C" {
#endif

#include "lvgl.h"


typedef struct
{
  
	lv_obj_t *screen;
	bool screen_del;
	lv_obj_t *screen_img_1;
	lv_obj_t *screen_1;
	bool screen_1_del;
	lv_obj_t *screen_1_img_1;
	lv_obj_t *screen_1_btn_1;
	lv_obj_t *screen_1_btn_1_label;
	lv_obj_t *screen_1_btn_2;
	lv_obj_t *screen_1_btn_2_label;
	lv_obj_t *screen_1_btn_3;
	lv_obj_t *screen_1_btn_3_label;
	lv_obj_t *screen_1_btn_4;
	lv_obj_t *screen_1_btn_4_label;
	lv_obj_t *screen_1_btn_5;
	lv_obj_t *screen_1_btn_5_label;
	lv_obj_t *screen_1_btn_6;
	lv_obj_t *screen_1_btn_6_label;
	lv_obj_t *screen_1_btn_7;
	lv_obj_t *screen_1_btn_7_label;
	lv_obj_t *screen_1_btn_8;
	lv_obj_t *screen_1_btn_8_label;
	lv_obj_t *screen_1_btn_9;
	lv_obj_t *screen_1_btn_9_label;
	lv_obj_t *screen_2;
	bool screen_2_del;
	lv_obj_t *screen_2_img_1;
	lv_obj_t *screen_2_btn_4;
	lv_obj_t *screen_2_btn_4_label;
	lv_obj_t *screen_2_btn_3;
	lv_obj_t *screen_2_btn_3_label;
	lv_obj_t *screen_2_btn_2;
	lv_obj_t *screen_2_btn_2_label;
	lv_obj_t *screen_2_btn_1;
	lv_obj_t *screen_2_btn_1_label;
	lv_obj_t *screen_3;
	bool screen_3_del;
	lv_obj_t *screen_3_img_1;
	lv_obj_t *screen_3_btn_4;
	lv_obj_t *screen_3_btn_4_label;
	lv_obj_t *screen_3_btn_3;
	lv_obj_t *screen_3_btn_3_label;
	lv_obj_t *screen_3_btn_2;
	lv_obj_t *screen_3_btn_2_label;
	lv_obj_t *screen_3_btn_1;
	lv_obj_t *screen_3_btn_1_label;
	lv_obj_t *screen_4;
	bool screen_4_del;
	lv_obj_t *screen_4_img_1;
	lv_obj_t *screen_4_btn_4;
	lv_obj_t *screen_4_btn_4_label;
	lv_obj_t *screen_4_btn_3;
	lv_obj_t *screen_4_btn_3_label;
	lv_obj_t *screen_4_btn_2;
	lv_obj_t *screen_4_btn_2_label;
	lv_obj_t *screen_4_btn_1;
	lv_obj_t *screen_4_btn_1_label;
	lv_obj_t *screen_5;
	bool screen_5_del;
	lv_obj_t *screen_5_img_1;
	lv_obj_t *screen_5_btn_4;
	lv_obj_t *screen_5_btn_4_label;
	lv_obj_t *screen_5_btn_3;
	lv_obj_t *screen_5_btn_3_label;
	lv_obj_t *screen_5_btn_2;
	lv_obj_t *screen_5_btn_2_label;
	lv_obj_t *screen_5_btn_1;
	lv_obj_t *screen_5_btn_1_label;
	lv_obj_t *screen_5_btn_5;
	lv_obj_t *screen_5_btn_5_label;
	lv_obj_t *screen_6;
	bool screen_6_del;
	lv_obj_t *screen_6_img_1;
	lv_obj_t *screen_6_btn_1;
	lv_obj_t *screen_6_btn_1_label;
	lv_obj_t *screen_7;
	bool screen_7_del;
	lv_obj_t *screen_7_img_1;
	lv_obj_t *screen_7_btn_4;
	lv_obj_t *screen_7_btn_4_label;
	lv_obj_t *screen_7_btn_3;
	lv_obj_t *screen_7_btn_3_label;
	lv_obj_t *screen_7_btn_2;
	lv_obj_t *screen_7_btn_2_label;
	lv_obj_t *screen_7_btn_1;
	lv_obj_t *screen_7_btn_1_label;
	lv_obj_t *screen_8;
	bool screen_8_del;
	lv_obj_t *screen_8_img_1;
	lv_obj_t *screen_8_btn_4;
	lv_obj_t *screen_8_btn_4_label;
	lv_obj_t *screen_8_btn_3;
	lv_obj_t *screen_8_btn_3_label;
	lv_obj_t *screen_8_btn_2;
	lv_obj_t *screen_8_btn_2_label;
	lv_obj_t *screen_8_btn_1;
	lv_obj_t *screen_8_btn_1_label;
	lv_obj_t *screen_8_btn_5;
	lv_obj_t *screen_8_btn_5_label;
	lv_obj_t *screen_9;
	bool screen_9_del;
	lv_obj_t *screen_9_img_1;
	lv_obj_t *screen_9_btn_4;
	lv_obj_t *screen_9_btn_4_label;
	lv_obj_t *screen_9_btn_3;
	lv_obj_t *screen_9_btn_3_label;
	lv_obj_t *screen_9_btn_2;
	lv_obj_t *screen_9_btn_2_label;
	lv_obj_t *screen_9_btn_1;
	lv_obj_t *screen_9_btn_1_label;
	lv_obj_t *screen_9_btn_5;
	lv_obj_t *screen_9_btn_5_label;
	lv_obj_t *screen_10;
	bool screen_10_del;
	lv_obj_t *screen_10_img_1;
	lv_obj_t *screen_10_btn_4;
	lv_obj_t *screen_10_btn_4_label;
	lv_obj_t *screen_10_btn_3;
	lv_obj_t *screen_10_btn_3_label;
	lv_obj_t *screen_10_btn_2;
	lv_obj_t *screen_10_btn_2_label;
	lv_obj_t *screen_10_btn_1;
	lv_obj_t *screen_10_btn_1_label;
	lv_obj_t *screen_11;
	bool screen_11_del;
	lv_obj_t *screen_11_img_1;
	lv_obj_t *screen_11_btn_4;
	lv_obj_t *screen_11_btn_4_label;
	lv_obj_t *screen_11_btn_3;
	lv_obj_t *screen_11_btn_3_label;
	lv_obj_t *screen_11_btn_2;
	lv_obj_t *screen_11_btn_2_label;
	lv_obj_t *screen_11_btn_1;
	lv_obj_t *screen_11_btn_1_label;
	lv_obj_t *screen_12;
	bool screen_12_del;
	lv_obj_t *screen_12_img_1;
	lv_obj_t *screen_12_btn_4;
	lv_obj_t *screen_12_btn_4_label;
	lv_obj_t *screen_12_btn_3;
	lv_obj_t *screen_12_btn_3_label;
	lv_obj_t *screen_12_btn_2;
	lv_obj_t *screen_12_btn_2_label;
	lv_obj_t *screen_12_btn_1;
	lv_obj_t *screen_12_btn_1_label;
	lv_obj_t *screen_13;
	bool screen_13_del;
	lv_obj_t *screen_13_img_1;
	lv_obj_t *screen_13_btn_4;
	lv_obj_t *screen_13_btn_4_label;
	lv_obj_t *screen_13_btn_3;
	lv_obj_t *screen_13_btn_3_label;
	lv_obj_t *screen_13_btn_2;
	lv_obj_t *screen_13_btn_2_label;
	lv_obj_t *screen_13_btn_1;
	lv_obj_t *screen_13_btn_1_label;
	lv_obj_t *screen_13_btn_5;
	lv_obj_t *screen_13_btn_5_label;
	lv_obj_t *screen_13_btn_6;
	lv_obj_t *screen_13_btn_6_label;
	lv_obj_t *screen_14;
	bool screen_14_del;
	lv_obj_t *screen_14_img_1;
	lv_obj_t *screen_14_btn_4;
	lv_obj_t *screen_14_btn_4_label;
	lv_obj_t *screen_14_btn_3;
	lv_obj_t *screen_14_btn_3_label;
	lv_obj_t *screen_14_btn_2;
	lv_obj_t *screen_14_btn_2_label;
	lv_obj_t *screen_14_btn_1;
	lv_obj_t *screen_14_btn_1_label;
	lv_obj_t *screen_14_btn_5;
	lv_obj_t *screen_14_btn_5_label;
	lv_obj_t *screen_15;
	bool screen_15_del;
	lv_obj_t *screen_15_img_1;
	lv_obj_t *screen_15_btn_4;
	lv_obj_t *screen_15_btn_4_label;
	lv_obj_t *screen_15_btn_3;
	lv_obj_t *screen_15_btn_3_label;
	lv_obj_t *screen_15_btn_2;
	lv_obj_t *screen_15_btn_2_label;
	lv_obj_t *screen_15_btn_1;
	lv_obj_t *screen_15_btn_1_label;
	lv_obj_t *screen_16;
	bool screen_16_del;
	lv_obj_t *screen_16_img_1;
	lv_obj_t *screen_16_btn_4;
	lv_obj_t *screen_16_btn_4_label;
	lv_obj_t *screen_16_btn_3;
	lv_obj_t *screen_16_btn_3_label;
	lv_obj_t *screen_16_btn_2;
	lv_obj_t *screen_16_btn_2_label;
	lv_obj_t *screen_16_btn_1;
	lv_obj_t *screen_16_btn_1_label;
	lv_obj_t *screen_16_btn_5;
	lv_obj_t *screen_16_btn_5_label;
	lv_obj_t *screen_17;
	bool screen_17_del;
	lv_obj_t *screen_17_img_1;
	lv_obj_t *screen_17_btn_4;
	lv_obj_t *screen_17_btn_4_label;
	lv_obj_t *screen_17_btn_3;
	lv_obj_t *screen_17_btn_3_label;
	lv_obj_t *screen_17_btn_2;
	lv_obj_t *screen_17_btn_2_label;
	lv_obj_t *screen_17_btn_1;
	lv_obj_t *screen_17_btn_1_label;
	lv_obj_t *screen_18;
	bool screen_18_del;
	lv_obj_t *screen_18_img_1;
	lv_obj_t *screen_18_btn_4;
	lv_obj_t *screen_18_btn_4_label;
	lv_obj_t *screen_18_btn_3;
	lv_obj_t *screen_18_btn_3_label;
	lv_obj_t *screen_18_btn_2;
	lv_obj_t *screen_18_btn_2_label;
	lv_obj_t *screen_18_btn_1;
	lv_obj_t *screen_18_btn_1_label;
	lv_obj_t *screen_19;
	bool screen_19_del;
	lv_obj_t *screen_19_img_1;
	lv_obj_t *screen_19_btn_4;
	lv_obj_t *screen_19_btn_4_label;
	lv_obj_t *screen_19_btn_3;
	lv_obj_t *screen_19_btn_3_label;
	lv_obj_t *screen_19_btn_2;
	lv_obj_t *screen_19_btn_2_label;
	lv_obj_t *screen_19_btn_1;
	lv_obj_t *screen_19_btn_1_label;
	lv_obj_t *screen_20;
	bool screen_20_del;
	lv_obj_t *screen_20_img_1;
	lv_obj_t *screen_20_btn_4;
	lv_obj_t *screen_20_btn_4_label;
	lv_obj_t *screen_20_btn_3;
	lv_obj_t *screen_20_btn_3_label;
	lv_obj_t *screen_20_btn_2;
	lv_obj_t *screen_20_btn_2_label;
	lv_obj_t *screen_20_btn_1;
	lv_obj_t *screen_20_btn_1_label;
	lv_obj_t *screen_21;
	bool screen_21_del;
	lv_obj_t *screen_21_img_1;
	lv_obj_t *screen_21_btn_4;
	lv_obj_t *screen_21_btn_4_label;
	lv_obj_t *screen_21_btn_3;
	lv_obj_t *screen_21_btn_3_label;
	lv_obj_t *screen_21_btn_2;
	lv_obj_t *screen_21_btn_2_label;
	lv_obj_t *screen_21_btn_1;
	lv_obj_t *screen_21_btn_1_label;
	lv_obj_t *screen_22;
	bool screen_22_del;
	lv_obj_t *screen_22_img_1;
	lv_obj_t *screen_22_btn_4;
	lv_obj_t *screen_22_btn_4_label;
	lv_obj_t *screen_22_btn_3;
	lv_obj_t *screen_22_btn_3_label;
	lv_obj_t *screen_22_btn_2;
	lv_obj_t *screen_22_btn_2_label;
	lv_obj_t *screen_22_btn_1;
	lv_obj_t *screen_22_btn_1_label;
	lv_obj_t *screen_23;
	bool screen_23_del;
	lv_obj_t *screen_23_img_1;
	lv_obj_t *screen_23_btn_4;
	lv_obj_t *screen_23_btn_4_label;
	lv_obj_t *screen_23_btn_3;
	lv_obj_t *screen_23_btn_3_label;
	lv_obj_t *screen_23_btn_2;
	lv_obj_t *screen_23_btn_2_label;
	lv_obj_t *screen_23_btn_1;
	lv_obj_t *screen_23_btn_1_label;
}lv_ui;

typedef void (*ui_setup_scr_t)(lv_ui * ui);

void ui_init_style(lv_style_t * style);

void ui_load_scr_animation(lv_ui *ui, lv_obj_t ** new_scr, bool new_scr_del, bool * old_scr_del, ui_setup_scr_t setup_scr,
                           lv_screen_load_anim_t anim_type, uint32_t time, uint32_t delay, bool is_clean, bool auto_del);

void ui_animation(void * var, uint32_t duration, int32_t delay, int32_t start_value, int32_t end_value, lv_anim_path_cb_t path_cb,
                  uint32_t repeat_cnt, uint32_t repeat_delay, uint32_t playback_time, uint32_t playback_delay,
                  lv_anim_exec_xcb_t exec_cb, lv_anim_start_cb_t start_cb, lv_anim_completed_cb_t ready_cb, lv_anim_deleted_cb_t deleted_cb);


void init_scr_del_flag(lv_ui *ui);

void setup_bottom_layer(void);

void setup_ui(lv_ui *ui);

void video_play(lv_ui *ui);

void init_keyboard(lv_ui *ui);

extern lv_ui guider_ui;


void setup_scr_screen(lv_ui *ui);
void setup_scr_screen_1(lv_ui *ui);
void setup_scr_screen_2(lv_ui *ui);
void setup_scr_screen_3(lv_ui *ui);
void setup_scr_screen_4(lv_ui *ui);
void setup_scr_screen_5(lv_ui *ui);
void setup_scr_screen_6(lv_ui *ui);
void setup_scr_screen_7(lv_ui *ui);
void setup_scr_screen_8(lv_ui *ui);
void setup_scr_screen_9(lv_ui *ui);
void setup_scr_screen_10(lv_ui *ui);
void setup_scr_screen_11(lv_ui *ui);
void setup_scr_screen_12(lv_ui *ui);
void setup_scr_screen_13(lv_ui *ui);
void setup_scr_screen_14(lv_ui *ui);
void setup_scr_screen_15(lv_ui *ui);
void setup_scr_screen_16(lv_ui *ui);
void setup_scr_screen_17(lv_ui *ui);
void setup_scr_screen_18(lv_ui *ui);
void setup_scr_screen_19(lv_ui *ui);
void setup_scr_screen_20(lv_ui *ui);
void setup_scr_screen_21(lv_ui *ui);
void setup_scr_screen_22(lv_ui *ui);
void setup_scr_screen_23(lv_ui *ui);
LV_IMAGE_DECLARE(_1_boot_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_2_anasayfa_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_3_rfid_bilgilendirme_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_4_qrkod_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_5_oyelik_detay_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_6_arac_baglantisi_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_7_haberlesme_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_8_haberlesme_hata_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_9_sarj_ana_ekran_beklemede_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_10_sarj_ana_ekran_sarj_ediyor_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_11_konnektor_bilgilendirme_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_12_rcd_hatasi_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_13_acil_durum_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_14_saj_durdur_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_15_sarj_ozeti_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_16_sarj_detaylari_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_17_bilgilendirme_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_18_nasil_sarj_ederim_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_19_rfid_kart_ile_sarj_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_20_mobil_uygulama_ile_sarj_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_21_dil_secimi_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_22_ayarlar_giris_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_23_ayarlar_ac_5_RGB565A8_800x480);
LV_IMAGE_DECLARE(_24_ag_ayarlari_ac_5_RGB565A8_800x480);

LV_FONT_DECLARE(lv_font_montserratMedium_16)
LV_FONT_DECLARE(lv_font_montserratMedium_12)


#ifdef __cplusplus
}
#endif
#endif
