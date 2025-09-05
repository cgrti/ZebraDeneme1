/*
* Copyright 2025 NXP
* NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
* accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
* activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
* comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
* terms, then you may not retain, install, activate or otherwise use the software.
*/

#include "events_init.h"
#include <stdio.h>
#include "lvgl.h"

#if LV_USE_GUIDER_SIMULATOR && LV_USE_FREEMASTER
#include "freemaster_client.h"
#endif


static void screen_img_1_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_1, guider_ui.screen_1_del, &guider_ui.screen_del, setup_scr_screen_1, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_screen (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->screen_img_1, screen_img_1_event_handler, LV_EVENT_ALL, ui);
}

static void screen_1_btn_1_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_17, guider_ui.screen_17_del, &guider_ui.screen_1_del, setup_scr_screen_17, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

static void screen_1_btn_2_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_2, guider_ui.screen_2_del, &guider_ui.screen_1_del, setup_scr_screen_2, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

static void screen_1_btn_3_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_3, guider_ui.screen_3_del, &guider_ui.screen_1_del, setup_scr_screen_3, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

static void screen_1_btn_4_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_4, guider_ui.screen_4_del, &guider_ui.screen_1_del, setup_scr_screen_4, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

static void screen_1_btn_9_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_5, guider_ui.screen_5_del, &guider_ui.screen_1_del, setup_scr_screen_5, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_screen_1 (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->screen_1_btn_1, screen_1_btn_1_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->screen_1_btn_2, screen_1_btn_2_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->screen_1_btn_3, screen_1_btn_3_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->screen_1_btn_4, screen_1_btn_4_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->screen_1_btn_9, screen_1_btn_9_event_handler, LV_EVENT_ALL, ui);
}

static void screen_5_btn_5_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_6, guider_ui.screen_6_del, &guider_ui.screen_5_del, setup_scr_screen_6, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_screen_5 (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->screen_5_btn_5, screen_5_btn_5_event_handler, LV_EVENT_ALL, ui);
}

static void screen_6_btn_1_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_8, guider_ui.screen_8_del, &guider_ui.screen_6_del, setup_scr_screen_8, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_screen_6 (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->screen_6_btn_1, screen_6_btn_1_event_handler, LV_EVENT_ALL, ui);
}

static void screen_8_btn_5_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_13, guider_ui.screen_13_del, &guider_ui.screen_8_del, setup_scr_screen_13, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_screen_8 (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->screen_8_btn_5, screen_8_btn_5_event_handler, LV_EVENT_ALL, ui);
}

static void screen_9_btn_5_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_13, guider_ui.screen_13_del, &guider_ui.screen_9_del, setup_scr_screen_13, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_screen_9 (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->screen_9_btn_5, screen_9_btn_5_event_handler, LV_EVENT_ALL, ui);
}

static void screen_13_btn_6_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_14, guider_ui.screen_14_del, &guider_ui.screen_13_del, setup_scr_screen_14, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_screen_13 (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->screen_13_btn_6, screen_13_btn_6_event_handler, LV_EVENT_ALL, ui);
}

static void screen_14_btn_5_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.screen_15, guider_ui.screen_15_del, &guider_ui.screen_14_del, setup_scr_screen_15, LV_SCR_LOAD_ANIM_NONE, 200, 200, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_screen_14 (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->screen_14_btn_5, screen_14_btn_5_event_handler, LV_EVENT_ALL, ui);
}

static void screen_16_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        break;
    }
    default:
        break;
    }
}

static void screen_16_btn_5_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        break;
    }
    default:
        break;
    }
}

void events_init_screen_16 (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->screen_16, screen_16_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->screen_16_btn_5, screen_16_btn_5_event_handler, LV_EVENT_ALL, ui);
}


void events_init(lv_ui *ui)
{

}
