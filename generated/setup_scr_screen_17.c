/*
* Copyright 2025 NXP
* NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
* accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
* activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
* comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
* terms, then you may not retain, install, activate or otherwise use the software.
*/

#include "lvgl.h"
#include <stdio.h>
#include "gui_guider.h"
#include "events_init.h"
#include "widgets_init.h"
#include "custom.h"



void setup_scr_screen_17(lv_ui *ui)
{
    //Write codes screen_17
    ui->screen_17 = lv_obj_create(NULL);
    lv_obj_set_size(ui->screen_17, 800, 480);
    lv_obj_set_scrollbar_mode(ui->screen_17, LV_SCROLLBAR_MODE_OFF);

    //Write style for screen_17, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->screen_17, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes screen_17_img_1
    ui->screen_17_img_1 = lv_image_create(ui->screen_17);
    lv_obj_set_pos(ui->screen_17_img_1, 0, 0);
    lv_obj_set_size(ui->screen_17_img_1, 800, 480);
    lv_obj_add_flag(ui->screen_17_img_1, LV_OBJ_FLAG_CLICKABLE);
    lv_image_set_src(ui->screen_17_img_1, &_18_nasil_sarj_ederim_ac_5_RGB565A8_800x480);
    lv_image_set_pivot(ui->screen_17_img_1, 50,50);
    lv_image_set_rotation(ui->screen_17_img_1, 0);

    //Write style for screen_17_img_1, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_image_recolor_opa(ui->screen_17_img_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_image_opa(ui->screen_17_img_1, 255, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes screen_17_btn_4
    ui->screen_17_btn_4 = lv_button_create(ui->screen_17);
    lv_obj_set_pos(ui->screen_17_btn_4, 215, 400);
    lv_obj_set_size(ui->screen_17_btn_4, 49, 48);
    ui->screen_17_btn_4_label = lv_label_create(ui->screen_17_btn_4);
    lv_label_set_text(ui->screen_17_btn_4_label, "");
    lv_label_set_long_mode(ui->screen_17_btn_4_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->screen_17_btn_4_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->screen_17_btn_4, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->screen_17_btn_4_label, LV_PCT(100));

    //Write style for screen_17_btn_4, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->screen_17_btn_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->screen_17_btn_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->screen_17_btn_4, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->screen_17_btn_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->screen_17_btn_4, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->screen_17_btn_4, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->screen_17_btn_4, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->screen_17_btn_4, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes screen_17_btn_3
    ui->screen_17_btn_3 = lv_button_create(ui->screen_17);
    lv_obj_set_pos(ui->screen_17_btn_3, 154, 400);
    lv_obj_set_size(ui->screen_17_btn_3, 49, 48);
    ui->screen_17_btn_3_label = lv_label_create(ui->screen_17_btn_3);
    lv_label_set_text(ui->screen_17_btn_3_label, "");
    lv_label_set_long_mode(ui->screen_17_btn_3_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->screen_17_btn_3_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->screen_17_btn_3, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->screen_17_btn_3_label, LV_PCT(100));

    //Write style for screen_17_btn_3, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->screen_17_btn_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->screen_17_btn_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->screen_17_btn_3, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->screen_17_btn_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->screen_17_btn_3, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->screen_17_btn_3, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->screen_17_btn_3, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->screen_17_btn_3, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes screen_17_btn_2
    ui->screen_17_btn_2 = lv_button_create(ui->screen_17);
    lv_obj_set_pos(ui->screen_17_btn_2, 32, 400);
    lv_obj_set_size(ui->screen_17_btn_2, 49, 48);
    ui->screen_17_btn_2_label = lv_label_create(ui->screen_17_btn_2);
    lv_label_set_text(ui->screen_17_btn_2_label, "");
    lv_label_set_long_mode(ui->screen_17_btn_2_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->screen_17_btn_2_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->screen_17_btn_2, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->screen_17_btn_2_label, LV_PCT(100));

    //Write style for screen_17_btn_2, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->screen_17_btn_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->screen_17_btn_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->screen_17_btn_2, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->screen_17_btn_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->screen_17_btn_2, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->screen_17_btn_2, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->screen_17_btn_2, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->screen_17_btn_2, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes screen_17_btn_1
    ui->screen_17_btn_1 = lv_button_create(ui->screen_17);
    lv_obj_set_pos(ui->screen_17_btn_1, 94, 400);
    lv_obj_set_size(ui->screen_17_btn_1, 49, 48);
    ui->screen_17_btn_1_label = lv_label_create(ui->screen_17_btn_1);
    lv_label_set_text(ui->screen_17_btn_1_label, "");
    lv_label_set_long_mode(ui->screen_17_btn_1_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->screen_17_btn_1_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->screen_17_btn_1, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->screen_17_btn_1_label, LV_PCT(100));

    //Write style for screen_17_btn_1, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->screen_17_btn_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->screen_17_btn_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->screen_17_btn_1, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->screen_17_btn_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->screen_17_btn_1, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->screen_17_btn_1, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->screen_17_btn_1, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->screen_17_btn_1, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //The custom code of screen_17.


    //Update current screen layout.
    lv_obj_update_layout(ui->screen_17);

}
