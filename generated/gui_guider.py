# Copyright 2025 NXP
# NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
# accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
# activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
# comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
# terms, then you may not retain, install, activate or otherwise use the software.

import utime as time
import usys as sys
import lvgl as lv
import ustruct
import fs_driver

lv.init()

# Register display driver.
disp_drv = lv.sdl_window_create(800, 480)
lv.sdl_window_set_resizeable(disp_drv, False)
lv.sdl_window_set_title(disp_drv, "Simulator (MicroPython)")

# Regsiter input driver
mouse = lv.sdl_mouse_create()

# Add default theme for bottom layer
bottom_layer = lv.layer_bottom()
lv.theme_apply(bottom_layer)

fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'Z')

def anim_x_cb(obj, v):
    obj.set_x(v)

def anim_y_cb(obj, v):
    obj.set_y(v)

def anim_width_cb(obj, v):
    obj.set_width(v)

def anim_height_cb(obj, v):
    obj.set_height(v)

def anim_img_zoom_cb(obj, v):
    obj.set_scale(v)

def anim_img_rotate_cb(obj, v):
    obj.set_rotation(v)

global_font_cache = {}
def test_font(font_family, font_size):
    global global_font_cache
    if font_family + str(font_size) in global_font_cache:
        return global_font_cache[font_family + str(font_size)]
    if font_size % 2:
        candidates = [
            (font_family, font_size),
            (font_family, font_size-font_size%2),
            (font_family, font_size+font_size%2),
            ("montserrat", font_size-font_size%2),
            ("montserrat", font_size+font_size%2),
            ("montserrat", 16)
        ]
    else:
        candidates = [
            (font_family, font_size),
            ("montserrat", font_size),
            ("montserrat", 16)
        ]
    for (family, size) in candidates:
        try:
            if eval(f'lv.font_{family}_{size}'):
                global_font_cache[font_family + str(font_size)] = eval(f'lv.font_{family}_{size}')
                if family != font_family or size != font_size:
                    print(f'WARNING: lv.font_{family}_{size} is used!')
                return eval(f'lv.font_{family}_{size}')
        except AttributeError:
            try:
                load_font = lv.binfont_create(f"Z:MicroPython/lv_font_{family}_{size}.fnt")
                global_font_cache[font_family + str(font_size)] = load_font
                return load_font
            except:
                if family == font_family and size == font_size:
                    print(f'WARNING: lv.font_{family}_{size} is NOT supported!')

global_image_cache = {}
def load_image(file):
    global global_image_cache
    if file in global_image_cache:
        return global_image_cache[file]
    try:
        with open(file,'rb') as f:
            data = f.read()
    except:
        print(f'Could not open {file}')
        sys.exit()

    img = lv.image_dsc_t({
        'data_size': len(data),
        'data': data
    })
    global_image_cache[file] = img
    return img

def calendar_event_handler(e,obj):
    code = e.get_code()

    if code == lv.EVENT.VALUE_CHANGED:
        source = lv.calendar.__cast__(e.get_current_target())
        date = lv.calendar_date_t()
        if source.get_pressed_date(date) == lv.RESULT.OK:
            source.set_highlighted_dates([date], 1)

def spinbox_increment_event_cb(e, obj):
    code = e.get_code()
    if code == lv.EVENT.SHORT_CLICKED or code == lv.EVENT.LONG_PRESSED_REPEAT:
        obj.increment()
def spinbox_decrement_event_cb(e, obj):
    code = e.get_code()
    if code == lv.EVENT.SHORT_CLICKED or code == lv.EVENT.LONG_PRESSED_REPEAT:
        obj.decrement()

def digital_clock_cb(timer, obj, current_time, show_second, use_ampm):
    hour = int(current_time[0])
    minute = int(current_time[1])
    second = int(current_time[2])
    ampm = current_time[3]
    second = second + 1
    if second == 60:
        second = 0
        minute = minute + 1
        if minute == 60:
            minute = 0
            hour = hour + 1
            if use_ampm:
                if hour == 12:
                    if ampm == 'AM':
                        ampm = 'PM'
                    elif ampm == 'PM':
                        ampm = 'AM'
                if hour > 12:
                    hour = hour % 12
    hour = hour % 24
    if use_ampm:
        if show_second:
            obj.set_text("%d:%02d:%02d %s" %(hour, minute, second, ampm))
        else:
            obj.set_text("%d:%02d %s" %(hour, minute, ampm))
    else:
        if show_second:
            obj.set_text("%d:%02d:%02d" %(hour, minute, second))
        else:
            obj.set_text("%d:%02d" %(hour, minute))
    current_time[0] = hour
    current_time[1] = minute
    current_time[2] = second
    current_time[3] = ampm

def analog_clock_cb(timer, obj):
    datetime = time.localtime()
    hour = datetime[3]
    if hour >= 12: hour = hour - 12
    obj.set_time(hour, datetime[4], datetime[5])

def datetext_event_handler(e, obj):
    code = e.get_code()
    datetext = lv.label.__cast__(e.get_target())
    if code == lv.EVENT.FOCUSED:
        if obj is None:
            bg = lv.layer_top()
            bg.add_flag(lv.obj.FLAG.CLICKABLE)
            obj = lv.calendar(bg)
            scr = lv.screen_active()
            scr_height = scr.get_height()
            scr_width = scr.get_width()
            obj.set_size(int(scr_width * 0.8), int(scr_height * 0.8))
            datestring = datetext.get_text()
            year = int(datestring.split('/')[0])
            month = int(datestring.split('/')[1])
            day = int(datestring.split('/')[2])
            obj.set_showed_date(year, month)
            highlighted_days=[lv.calendar_date_t({'year':year, 'month':month, 'day':day})]
            obj.set_highlighted_dates(highlighted_days, 1)
            obj.align(lv.ALIGN.CENTER, 0, 0)
            lv.calendar_header_arrow(obj)
            obj.add_event_cb(lambda e: datetext_calendar_event_handler(e, datetext), lv.EVENT.ALL, None)
            scr.update_layout()

def datetext_calendar_event_handler(e, obj):
    code = e.get_code()
    calendar = lv.calendar.__cast__(e.get_current_target())
    if code == lv.EVENT.VALUE_CHANGED:
        date = lv.calendar_date_t()
        if calendar.get_pressed_date(date) == lv.RESULT.OK:
            obj.set_text(f"{date.year}/{date.month}/{date.day}")
            bg = lv.layer_top()
            bg.remove_flag(lv.obj.FLAG.CLICKABLE)
            bg.set_style_bg_opa(lv.OPA.TRANSP, 0)
            calendar.delete()

# Create screen
screen = lv.obj()
screen.set_size(800, 480)
screen.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_img_1
screen_img_1 = lv.image(screen)
screen_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\1_boot_ac_5_800_480.png"))
screen_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_img_1.set_pivot(50,50)
screen_img_1.set_rotation(0)
screen_img_1.set_pos(0, 0)
screen_img_1.set_size(800, 480)
# Set style for screen_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

screen.update_layout()
# Create screen_1
screen_1 = lv.obj()
screen_1.set_size(800, 480)
screen_1.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_img_1
screen_1_img_1 = lv.image(screen_1)
screen_1_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\2_anasayfa_ac_5_800_480.png"))
screen_1_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_1_img_1.set_pivot(50,50)
screen_1_img_1.set_rotation(0)
screen_1_img_1.set_pos(0, 0)
screen_1_img_1.set_size(800, 480)
# Set style for screen_1_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_1
screen_1_btn_1 = lv.button(screen_1)
screen_1_btn_1_label = lv.label(screen_1_btn_1)
screen_1_btn_1_label.set_text("")
screen_1_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_1_btn_1_label.set_width(lv.pct(100))
screen_1_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_1.set_pos(285, 400)
screen_1_btn_1.set_size(230, 44)
# Set style for screen_1_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_2
screen_1_btn_2 = lv.button(screen_1)
screen_1_btn_2_label = lv.label(screen_1_btn_2)
screen_1_btn_2_label.set_text("")
screen_1_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_1_btn_2_label.set_width(lv.pct(100))
screen_1_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_2.set_pos(52, 132)
screen_1_btn_2.set_size(188, 219)
# Set style for screen_1_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_3
screen_1_btn_3 = lv.button(screen_1)
screen_1_btn_3_label = lv.label(screen_1_btn_3)
screen_1_btn_3_label.set_text("")
screen_1_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_1_btn_3_label.set_width(lv.pct(100))
screen_1_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_3.set_pos(308, 132)
screen_1_btn_3.set_size(188, 219)
# Set style for screen_1_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_4
screen_1_btn_4 = lv.button(screen_1)
screen_1_btn_4_label = lv.label(screen_1_btn_4)
screen_1_btn_4_label.set_text("")
screen_1_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_1_btn_4_label.set_width(lv.pct(100))
screen_1_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_4.set_pos(560, 132)
screen_1_btn_4.set_size(188, 219)
# Set style for screen_1_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_5
screen_1_btn_5 = lv.button(screen_1)
screen_1_btn_5_label = lv.label(screen_1_btn_5)
screen_1_btn_5_label.set_text("")
screen_1_btn_5_label.set_long_mode(lv.label.LONG.WRAP)
screen_1_btn_5_label.set_width(lv.pct(100))
screen_1_btn_5_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_5.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_5.set_pos(32, 400)
screen_1_btn_5.set_size(49, 48)
# Set style for screen_1_btn_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_5.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_5.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_5.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_5.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_5.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_5.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_5.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_6
screen_1_btn_6 = lv.button(screen_1)
screen_1_btn_6_label = lv.label(screen_1_btn_6)
screen_1_btn_6_label.set_text("")
screen_1_btn_6_label.set_long_mode(lv.label.LONG.WRAP)
screen_1_btn_6_label.set_width(lv.pct(100))
screen_1_btn_6_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_6.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_6.set_pos(94, 400)
screen_1_btn_6.set_size(49, 48)
# Set style for screen_1_btn_6, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_6.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_6.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_6.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_6.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_6.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_6.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_6.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_6.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_7
screen_1_btn_7 = lv.button(screen_1)
screen_1_btn_7_label = lv.label(screen_1_btn_7)
screen_1_btn_7_label.set_text("")
screen_1_btn_7_label.set_long_mode(lv.label.LONG.WRAP)
screen_1_btn_7_label.set_width(lv.pct(100))
screen_1_btn_7_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_7.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_7.set_pos(154, 400)
screen_1_btn_7.set_size(49, 48)
# Set style for screen_1_btn_7, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_7.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_7.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_7.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_7.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_7.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_7.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_7.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_7.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_8
screen_1_btn_8 = lv.button(screen_1)
screen_1_btn_8_label = lv.label(screen_1_btn_8)
screen_1_btn_8_label.set_text("")
screen_1_btn_8_label.set_long_mode(lv.label.LONG.WRAP)
screen_1_btn_8_label.set_width(lv.pct(100))
screen_1_btn_8_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_8.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_8.set_pos(215, 400)
screen_1_btn_8.set_size(49, 48)
# Set style for screen_1_btn_8, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_8.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_8.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_8.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_8.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_8.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_8.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_8.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_8.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_9
screen_1_btn_9 = lv.button(screen_1)
screen_1_btn_9_label = lv.label(screen_1_btn_9)
screen_1_btn_9_label.set_text("")
screen_1_btn_9_label.set_long_mode(lv.label.LONG.WRAP)
screen_1_btn_9_label.set_width(lv.pct(100))
screen_1_btn_9_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_9.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_9.set_pos(11, 31)
screen_1_btn_9.set_size(775, 53)
# Set style for screen_1_btn_9, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_9.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_9.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_9.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_9.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_9.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_9.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_9.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_9.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_1.update_layout()
# Create screen_2
screen_2 = lv.obj()
screen_2.set_size(800, 480)
screen_2.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_2_img_1
screen_2_img_1 = lv.image(screen_2)
screen_2_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\3_rfid_bilgilendirme_ac_5_800_480.png"))
screen_2_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_2_img_1.set_pivot(50,50)
screen_2_img_1.set_rotation(0)
screen_2_img_1.set_pos(0, 0)
screen_2_img_1.set_size(800, 480)
# Set style for screen_2_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_2_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_2_btn_4
screen_2_btn_4 = lv.button(screen_2)
screen_2_btn_4_label = lv.label(screen_2_btn_4)
screen_2_btn_4_label.set_text("")
screen_2_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_2_btn_4_label.set_width(lv.pct(100))
screen_2_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_2_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_2_btn_4.set_pos(215, 400)
screen_2_btn_4.set_size(49, 48)
# Set style for screen_2_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_2_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_2_btn_3
screen_2_btn_3 = lv.button(screen_2)
screen_2_btn_3_label = lv.label(screen_2_btn_3)
screen_2_btn_3_label.set_text("")
screen_2_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_2_btn_3_label.set_width(lv.pct(100))
screen_2_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_2_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_2_btn_3.set_pos(154, 400)
screen_2_btn_3.set_size(49, 48)
# Set style for screen_2_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_2_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_2_btn_2
screen_2_btn_2 = lv.button(screen_2)
screen_2_btn_2_label = lv.label(screen_2_btn_2)
screen_2_btn_2_label.set_text("")
screen_2_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_2_btn_2_label.set_width(lv.pct(100))
screen_2_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_2_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_2_btn_2.set_pos(32, 400)
screen_2_btn_2.set_size(49, 48)
# Set style for screen_2_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_2_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_2_btn_1
screen_2_btn_1 = lv.button(screen_2)
screen_2_btn_1_label = lv.label(screen_2_btn_1)
screen_2_btn_1_label.set_text("")
screen_2_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_2_btn_1_label.set_width(lv.pct(100))
screen_2_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_2_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_2_btn_1.set_pos(94, 400)
screen_2_btn_1.set_size(49, 48)
# Set style for screen_2_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_2_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_2_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_2.update_layout()
# Create screen_3
screen_3 = lv.obj()
screen_3.set_size(800, 480)
screen_3.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_3_img_1
screen_3_img_1 = lv.image(screen_3)
screen_3_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\4_qrkod_ac_5_800_480.png"))
screen_3_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_3_img_1.set_pivot(50,50)
screen_3_img_1.set_rotation(0)
screen_3_img_1.set_pos(0, 0)
screen_3_img_1.set_size(800, 480)
# Set style for screen_3_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_3_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_3_btn_4
screen_3_btn_4 = lv.button(screen_3)
screen_3_btn_4_label = lv.label(screen_3_btn_4)
screen_3_btn_4_label.set_text("")
screen_3_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_3_btn_4_label.set_width(lv.pct(100))
screen_3_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_3_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_3_btn_4.set_pos(215, 400)
screen_3_btn_4.set_size(49, 48)
# Set style for screen_3_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_3_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_3_btn_3
screen_3_btn_3 = lv.button(screen_3)
screen_3_btn_3_label = lv.label(screen_3_btn_3)
screen_3_btn_3_label.set_text("")
screen_3_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_3_btn_3_label.set_width(lv.pct(100))
screen_3_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_3_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_3_btn_3.set_pos(154, 400)
screen_3_btn_3.set_size(49, 48)
# Set style for screen_3_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_3_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_3_btn_2
screen_3_btn_2 = lv.button(screen_3)
screen_3_btn_2_label = lv.label(screen_3_btn_2)
screen_3_btn_2_label.set_text("")
screen_3_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_3_btn_2_label.set_width(lv.pct(100))
screen_3_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_3_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_3_btn_2.set_pos(32, 400)
screen_3_btn_2.set_size(49, 48)
# Set style for screen_3_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_3_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_3_btn_1
screen_3_btn_1 = lv.button(screen_3)
screen_3_btn_1_label = lv.label(screen_3_btn_1)
screen_3_btn_1_label.set_text("")
screen_3_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_3_btn_1_label.set_width(lv.pct(100))
screen_3_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_3_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_3_btn_1.set_pos(94, 400)
screen_3_btn_1.set_size(49, 48)
# Set style for screen_3_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_3_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_3_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_3.update_layout()
# Create screen_4
screen_4 = lv.obj()
screen_4.set_size(800, 480)
screen_4.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_4_img_1
screen_4_img_1 = lv.image(screen_4)
screen_4_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\5_oyelik_detay_ac_5_800_480.png"))
screen_4_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_4_img_1.set_pivot(50,50)
screen_4_img_1.set_rotation(0)
screen_4_img_1.set_pos(0, 0)
screen_4_img_1.set_size(800, 480)
# Set style for screen_4_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_4_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_4_btn_4
screen_4_btn_4 = lv.button(screen_4)
screen_4_btn_4_label = lv.label(screen_4_btn_4)
screen_4_btn_4_label.set_text("")
screen_4_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_4_btn_4_label.set_width(lv.pct(100))
screen_4_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_4_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_4_btn_4.set_pos(215, 400)
screen_4_btn_4.set_size(49, 48)
# Set style for screen_4_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_4_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_4_btn_3
screen_4_btn_3 = lv.button(screen_4)
screen_4_btn_3_label = lv.label(screen_4_btn_3)
screen_4_btn_3_label.set_text("")
screen_4_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_4_btn_3_label.set_width(lv.pct(100))
screen_4_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_4_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_4_btn_3.set_pos(154, 400)
screen_4_btn_3.set_size(49, 48)
# Set style for screen_4_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_4_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_4_btn_2
screen_4_btn_2 = lv.button(screen_4)
screen_4_btn_2_label = lv.label(screen_4_btn_2)
screen_4_btn_2_label.set_text("")
screen_4_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_4_btn_2_label.set_width(lv.pct(100))
screen_4_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_4_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_4_btn_2.set_pos(32, 400)
screen_4_btn_2.set_size(49, 48)
# Set style for screen_4_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_4_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_4_btn_1
screen_4_btn_1 = lv.button(screen_4)
screen_4_btn_1_label = lv.label(screen_4_btn_1)
screen_4_btn_1_label.set_text("")
screen_4_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_4_btn_1_label.set_width(lv.pct(100))
screen_4_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_4_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_4_btn_1.set_pos(94, 400)
screen_4_btn_1.set_size(49, 48)
# Set style for screen_4_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_4_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_4_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_4.update_layout()
# Create screen_5
screen_5 = lv.obj()
screen_5.set_size(800, 480)
screen_5.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_5.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_5_img_1
screen_5_img_1 = lv.image(screen_5)
screen_5_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\6_arac_baglantisi_ac_5_800_480.png"))
screen_5_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_5_img_1.set_pivot(50,50)
screen_5_img_1.set_rotation(0)
screen_5_img_1.set_pos(0, 0)
screen_5_img_1.set_size(800, 480)
# Set style for screen_5_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_5_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_5_btn_4
screen_5_btn_4 = lv.button(screen_5)
screen_5_btn_4_label = lv.label(screen_5_btn_4)
screen_5_btn_4_label.set_text("")
screen_5_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_5_btn_4_label.set_width(lv.pct(100))
screen_5_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_5_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_5_btn_4.set_pos(215, 400)
screen_5_btn_4.set_size(49, 48)
# Set style for screen_5_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_5_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_5_btn_3
screen_5_btn_3 = lv.button(screen_5)
screen_5_btn_3_label = lv.label(screen_5_btn_3)
screen_5_btn_3_label.set_text("")
screen_5_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_5_btn_3_label.set_width(lv.pct(100))
screen_5_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_5_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_5_btn_3.set_pos(154, 400)
screen_5_btn_3.set_size(49, 48)
# Set style for screen_5_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_5_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_5_btn_2
screen_5_btn_2 = lv.button(screen_5)
screen_5_btn_2_label = lv.label(screen_5_btn_2)
screen_5_btn_2_label.set_text("")
screen_5_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_5_btn_2_label.set_width(lv.pct(100))
screen_5_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_5_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_5_btn_2.set_pos(32, 400)
screen_5_btn_2.set_size(49, 48)
# Set style for screen_5_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_5_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_5_btn_1
screen_5_btn_1 = lv.button(screen_5)
screen_5_btn_1_label = lv.label(screen_5_btn_1)
screen_5_btn_1_label.set_text("")
screen_5_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_5_btn_1_label.set_width(lv.pct(100))
screen_5_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_5_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_5_btn_1.set_pos(94, 400)
screen_5_btn_1.set_size(49, 48)
# Set style for screen_5_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_5_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_5_btn_5
screen_5_btn_5 = lv.button(screen_5)
screen_5_btn_5_label = lv.label(screen_5_btn_5)
screen_5_btn_5_label.set_text("")
screen_5_btn_5_label.set_long_mode(lv.label.LONG.WRAP)
screen_5_btn_5_label.set_width(lv.pct(100))
screen_5_btn_5_label.align(lv.ALIGN.CENTER, 0, 0)
screen_5_btn_5.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_5_btn_5.set_pos(203, 127)
screen_5_btn_5.set_size(389, 219)
# Set style for screen_5_btn_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_5_btn_5.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_5.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_5.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_5.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_5.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_5.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_5.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_5_btn_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_5.update_layout()
# Create screen_6
screen_6 = lv.obj()
screen_6.set_size(800, 480)
screen_6.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_6, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_6.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_6_img_1
screen_6_img_1 = lv.image(screen_6)
screen_6_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\7_haberlesme_ac_5_800_480.png"))
screen_6_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_6_img_1.set_pivot(50,50)
screen_6_img_1.set_rotation(0)
screen_6_img_1.set_pos(0, 0)
screen_6_img_1.set_size(800, 480)
# Set style for screen_6_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_6_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_6_btn_1
screen_6_btn_1 = lv.button(screen_6)
screen_6_btn_1_label = lv.label(screen_6_btn_1)
screen_6_btn_1_label.set_text("")
screen_6_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_6_btn_1_label.set_width(lv.pct(100))
screen_6_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_6_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_6_btn_1.set_pos(307, 113)
screen_6_btn_1.set_size(188, 246)
# Set style for screen_6_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_6_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_6_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_6_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_6_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_6_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_6_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_6_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_6_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_6.update_layout()
# Create screen_7
screen_7 = lv.obj()
screen_7.set_size(800, 480)
screen_7.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_7, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_7.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_7_img_1
screen_7_img_1 = lv.image(screen_7)
screen_7_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\8_haberlesme_hata_ac_5_800_480.png"))
screen_7_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_7_img_1.set_pivot(50,50)
screen_7_img_1.set_rotation(0)
screen_7_img_1.set_pos(0, 0)
screen_7_img_1.set_size(800, 480)
# Set style for screen_7_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_7_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_7_btn_4
screen_7_btn_4 = lv.button(screen_7)
screen_7_btn_4_label = lv.label(screen_7_btn_4)
screen_7_btn_4_label.set_text("")
screen_7_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_7_btn_4_label.set_width(lv.pct(100))
screen_7_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_7_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_7_btn_4.set_pos(215, 400)
screen_7_btn_4.set_size(49, 48)
# Set style for screen_7_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_7_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_7_btn_3
screen_7_btn_3 = lv.button(screen_7)
screen_7_btn_3_label = lv.label(screen_7_btn_3)
screen_7_btn_3_label.set_text("")
screen_7_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_7_btn_3_label.set_width(lv.pct(100))
screen_7_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_7_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_7_btn_3.set_pos(154, 400)
screen_7_btn_3.set_size(49, 48)
# Set style for screen_7_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_7_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_7_btn_2
screen_7_btn_2 = lv.button(screen_7)
screen_7_btn_2_label = lv.label(screen_7_btn_2)
screen_7_btn_2_label.set_text("")
screen_7_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_7_btn_2_label.set_width(lv.pct(100))
screen_7_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_7_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_7_btn_2.set_pos(32, 400)
screen_7_btn_2.set_size(49, 48)
# Set style for screen_7_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_7_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_7_btn_1
screen_7_btn_1 = lv.button(screen_7)
screen_7_btn_1_label = lv.label(screen_7_btn_1)
screen_7_btn_1_label.set_text("")
screen_7_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_7_btn_1_label.set_width(lv.pct(100))
screen_7_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_7_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_7_btn_1.set_pos(94, 400)
screen_7_btn_1.set_size(49, 48)
# Set style for screen_7_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_7_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_7_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_7.update_layout()
# Create screen_8
screen_8 = lv.obj()
screen_8.set_size(800, 480)
screen_8.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_8, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_8.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_8_img_1
screen_8_img_1 = lv.image(screen_8)
screen_8_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\9_sarj_ana_ekran_beklemede_ac_5_800_480.png"))
screen_8_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_8_img_1.set_pivot(50,50)
screen_8_img_1.set_rotation(0)
screen_8_img_1.set_pos(0, 0)
screen_8_img_1.set_size(800, 480)
# Set style for screen_8_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_8_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_8_btn_4
screen_8_btn_4 = lv.button(screen_8)
screen_8_btn_4_label = lv.label(screen_8_btn_4)
screen_8_btn_4_label.set_text("")
screen_8_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_8_btn_4_label.set_width(lv.pct(100))
screen_8_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_8_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_8_btn_4.set_pos(215, 400)
screen_8_btn_4.set_size(49, 48)
# Set style for screen_8_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_8_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_8_btn_3
screen_8_btn_3 = lv.button(screen_8)
screen_8_btn_3_label = lv.label(screen_8_btn_3)
screen_8_btn_3_label.set_text("")
screen_8_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_8_btn_3_label.set_width(lv.pct(100))
screen_8_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_8_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_8_btn_3.set_pos(154, 400)
screen_8_btn_3.set_size(49, 48)
# Set style for screen_8_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_8_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_8_btn_2
screen_8_btn_2 = lv.button(screen_8)
screen_8_btn_2_label = lv.label(screen_8_btn_2)
screen_8_btn_2_label.set_text("")
screen_8_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_8_btn_2_label.set_width(lv.pct(100))
screen_8_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_8_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_8_btn_2.set_pos(32, 400)
screen_8_btn_2.set_size(49, 48)
# Set style for screen_8_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_8_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_8_btn_1
screen_8_btn_1 = lv.button(screen_8)
screen_8_btn_1_label = lv.label(screen_8_btn_1)
screen_8_btn_1_label.set_text("")
screen_8_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_8_btn_1_label.set_width(lv.pct(100))
screen_8_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_8_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_8_btn_1.set_pos(94, 400)
screen_8_btn_1.set_size(49, 48)
# Set style for screen_8_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_8_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_8_btn_5
screen_8_btn_5 = lv.button(screen_8)
screen_8_btn_5_label = lv.label(screen_8_btn_5)
screen_8_btn_5_label.set_text("")
screen_8_btn_5_label.set_long_mode(lv.label.LONG.WRAP)
screen_8_btn_5_label.set_width(lv.pct(100))
screen_8_btn_5_label.align(lv.ALIGN.CENTER, 0, 0)
screen_8_btn_5.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_8_btn_5.set_pos(285, 400)
screen_8_btn_5.set_size(229, 48)
# Set style for screen_8_btn_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_8_btn_5.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_5.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_5.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_5.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_5.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_5.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_5.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_8_btn_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_8.update_layout()
# Create screen_9
screen_9 = lv.obj()
screen_9.set_size(800, 480)
screen_9.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_9, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_9.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_9_img_1
screen_9_img_1 = lv.image(screen_9)
screen_9_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\10_sarj_ana_ekran_sarj_ediyor_ac_5_800_480.png"))
screen_9_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_9_img_1.set_pivot(50,50)
screen_9_img_1.set_rotation(0)
screen_9_img_1.set_pos(0, 0)
screen_9_img_1.set_size(800, 480)
# Set style for screen_9_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_9_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_9_btn_4
screen_9_btn_4 = lv.button(screen_9)
screen_9_btn_4_label = lv.label(screen_9_btn_4)
screen_9_btn_4_label.set_text("")
screen_9_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_9_btn_4_label.set_width(lv.pct(100))
screen_9_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_9_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_9_btn_4.set_pos(215, 400)
screen_9_btn_4.set_size(49, 48)
# Set style for screen_9_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_9_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_9_btn_3
screen_9_btn_3 = lv.button(screen_9)
screen_9_btn_3_label = lv.label(screen_9_btn_3)
screen_9_btn_3_label.set_text("")
screen_9_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_9_btn_3_label.set_width(lv.pct(100))
screen_9_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_9_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_9_btn_3.set_pos(154, 400)
screen_9_btn_3.set_size(49, 48)
# Set style for screen_9_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_9_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_9_btn_2
screen_9_btn_2 = lv.button(screen_9)
screen_9_btn_2_label = lv.label(screen_9_btn_2)
screen_9_btn_2_label.set_text("")
screen_9_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_9_btn_2_label.set_width(lv.pct(100))
screen_9_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_9_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_9_btn_2.set_pos(32, 400)
screen_9_btn_2.set_size(49, 48)
# Set style for screen_9_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_9_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_9_btn_1
screen_9_btn_1 = lv.button(screen_9)
screen_9_btn_1_label = lv.label(screen_9_btn_1)
screen_9_btn_1_label.set_text("")
screen_9_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_9_btn_1_label.set_width(lv.pct(100))
screen_9_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_9_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_9_btn_1.set_pos(94, 400)
screen_9_btn_1.set_size(49, 48)
# Set style for screen_9_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_9_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_9_btn_5
screen_9_btn_5 = lv.button(screen_9)
screen_9_btn_5_label = lv.label(screen_9_btn_5)
screen_9_btn_5_label.set_text("")
screen_9_btn_5_label.set_long_mode(lv.label.LONG.WRAP)
screen_9_btn_5_label.set_width(lv.pct(100))
screen_9_btn_5_label.align(lv.ALIGN.CENTER, 0, 0)
screen_9_btn_5.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_9_btn_5.set_pos(285, 400)
screen_9_btn_5.set_size(229, 48)
# Set style for screen_9_btn_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_9_btn_5.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_5.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_5.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_5.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_5.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_5.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_5.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_9_btn_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_9.update_layout()
# Create screen_10
screen_10 = lv.obj()
screen_10.set_size(800, 480)
screen_10.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_10, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_10.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_10_img_1
screen_10_img_1 = lv.image(screen_10)
screen_10_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\11_konnektor_bilgilendirme_ac_5_800_480.png"))
screen_10_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_10_img_1.set_pivot(50,50)
screen_10_img_1.set_rotation(0)
screen_10_img_1.set_pos(0, 0)
screen_10_img_1.set_size(800, 480)
# Set style for screen_10_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_10_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_10_btn_4
screen_10_btn_4 = lv.button(screen_10)
screen_10_btn_4_label = lv.label(screen_10_btn_4)
screen_10_btn_4_label.set_text("")
screen_10_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_10_btn_4_label.set_width(lv.pct(100))
screen_10_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_10_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_10_btn_4.set_pos(215, 400)
screen_10_btn_4.set_size(49, 48)
# Set style for screen_10_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_10_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_10_btn_3
screen_10_btn_3 = lv.button(screen_10)
screen_10_btn_3_label = lv.label(screen_10_btn_3)
screen_10_btn_3_label.set_text("")
screen_10_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_10_btn_3_label.set_width(lv.pct(100))
screen_10_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_10_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_10_btn_3.set_pos(154, 400)
screen_10_btn_3.set_size(49, 48)
# Set style for screen_10_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_10_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_10_btn_2
screen_10_btn_2 = lv.button(screen_10)
screen_10_btn_2_label = lv.label(screen_10_btn_2)
screen_10_btn_2_label.set_text("")
screen_10_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_10_btn_2_label.set_width(lv.pct(100))
screen_10_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_10_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_10_btn_2.set_pos(32, 400)
screen_10_btn_2.set_size(49, 48)
# Set style for screen_10_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_10_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_10_btn_1
screen_10_btn_1 = lv.button(screen_10)
screen_10_btn_1_label = lv.label(screen_10_btn_1)
screen_10_btn_1_label.set_text("")
screen_10_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_10_btn_1_label.set_width(lv.pct(100))
screen_10_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_10_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_10_btn_1.set_pos(94, 400)
screen_10_btn_1.set_size(49, 48)
# Set style for screen_10_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_10_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_10_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_10.update_layout()
# Create screen_11
screen_11 = lv.obj()
screen_11.set_size(800, 480)
screen_11.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_11, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_11.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_11_img_1
screen_11_img_1 = lv.image(screen_11)
screen_11_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\12_rcd_hatasi_ac_5_800_480.png"))
screen_11_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_11_img_1.set_pivot(50,50)
screen_11_img_1.set_rotation(0)
screen_11_img_1.set_pos(0, 0)
screen_11_img_1.set_size(800, 480)
# Set style for screen_11_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_11_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_11_btn_4
screen_11_btn_4 = lv.button(screen_11)
screen_11_btn_4_label = lv.label(screen_11_btn_4)
screen_11_btn_4_label.set_text("")
screen_11_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_11_btn_4_label.set_width(lv.pct(100))
screen_11_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_11_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_11_btn_4.set_pos(215, 400)
screen_11_btn_4.set_size(49, 48)
# Set style for screen_11_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_11_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_11_btn_3
screen_11_btn_3 = lv.button(screen_11)
screen_11_btn_3_label = lv.label(screen_11_btn_3)
screen_11_btn_3_label.set_text("")
screen_11_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_11_btn_3_label.set_width(lv.pct(100))
screen_11_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_11_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_11_btn_3.set_pos(154, 400)
screen_11_btn_3.set_size(49, 48)
# Set style for screen_11_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_11_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_11_btn_2
screen_11_btn_2 = lv.button(screen_11)
screen_11_btn_2_label = lv.label(screen_11_btn_2)
screen_11_btn_2_label.set_text("")
screen_11_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_11_btn_2_label.set_width(lv.pct(100))
screen_11_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_11_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_11_btn_2.set_pos(32, 400)
screen_11_btn_2.set_size(49, 48)
# Set style for screen_11_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_11_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_11_btn_1
screen_11_btn_1 = lv.button(screen_11)
screen_11_btn_1_label = lv.label(screen_11_btn_1)
screen_11_btn_1_label.set_text("")
screen_11_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_11_btn_1_label.set_width(lv.pct(100))
screen_11_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_11_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_11_btn_1.set_pos(94, 400)
screen_11_btn_1.set_size(49, 48)
# Set style for screen_11_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_11_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_11_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_11.update_layout()
# Create screen_12
screen_12 = lv.obj()
screen_12.set_size(800, 480)
screen_12.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_12, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_12.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_12_img_1
screen_12_img_1 = lv.image(screen_12)
screen_12_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\13_acil_durum_ac_5_800_480.png"))
screen_12_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_12_img_1.set_pivot(50,50)
screen_12_img_1.set_rotation(0)
screen_12_img_1.set_pos(0, 0)
screen_12_img_1.set_size(800, 480)
# Set style for screen_12_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_12_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_12_btn_4
screen_12_btn_4 = lv.button(screen_12)
screen_12_btn_4_label = lv.label(screen_12_btn_4)
screen_12_btn_4_label.set_text("")
screen_12_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_12_btn_4_label.set_width(lv.pct(100))
screen_12_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_12_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_12_btn_4.set_pos(215, 400)
screen_12_btn_4.set_size(49, 48)
# Set style for screen_12_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_12_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_12_btn_3
screen_12_btn_3 = lv.button(screen_12)
screen_12_btn_3_label = lv.label(screen_12_btn_3)
screen_12_btn_3_label.set_text("")
screen_12_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_12_btn_3_label.set_width(lv.pct(100))
screen_12_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_12_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_12_btn_3.set_pos(154, 400)
screen_12_btn_3.set_size(49, 48)
# Set style for screen_12_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_12_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_12_btn_2
screen_12_btn_2 = lv.button(screen_12)
screen_12_btn_2_label = lv.label(screen_12_btn_2)
screen_12_btn_2_label.set_text("")
screen_12_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_12_btn_2_label.set_width(lv.pct(100))
screen_12_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_12_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_12_btn_2.set_pos(32, 400)
screen_12_btn_2.set_size(49, 48)
# Set style for screen_12_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_12_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_12_btn_1
screen_12_btn_1 = lv.button(screen_12)
screen_12_btn_1_label = lv.label(screen_12_btn_1)
screen_12_btn_1_label.set_text("")
screen_12_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_12_btn_1_label.set_width(lv.pct(100))
screen_12_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_12_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_12_btn_1.set_pos(94, 400)
screen_12_btn_1.set_size(49, 48)
# Set style for screen_12_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_12_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_12_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_12.update_layout()
# Create screen_13
screen_13 = lv.obj()
screen_13.set_size(800, 480)
screen_13.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_13, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_13.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_13_img_1
screen_13_img_1 = lv.image(screen_13)
screen_13_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\14_saj_durdur_ac_5_800_480.png"))
screen_13_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_13_img_1.set_pivot(50,50)
screen_13_img_1.set_rotation(0)
screen_13_img_1.set_pos(0, 0)
screen_13_img_1.set_size(800, 480)
# Set style for screen_13_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_13_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_13_btn_4
screen_13_btn_4 = lv.button(screen_13)
screen_13_btn_4_label = lv.label(screen_13_btn_4)
screen_13_btn_4_label.set_text("")
screen_13_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_13_btn_4_label.set_width(lv.pct(100))
screen_13_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_13_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_13_btn_4.set_pos(215, 400)
screen_13_btn_4.set_size(49, 48)
# Set style for screen_13_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_13_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_13_btn_3
screen_13_btn_3 = lv.button(screen_13)
screen_13_btn_3_label = lv.label(screen_13_btn_3)
screen_13_btn_3_label.set_text("")
screen_13_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_13_btn_3_label.set_width(lv.pct(100))
screen_13_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_13_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_13_btn_3.set_pos(154, 400)
screen_13_btn_3.set_size(49, 48)
# Set style for screen_13_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_13_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_13_btn_2
screen_13_btn_2 = lv.button(screen_13)
screen_13_btn_2_label = lv.label(screen_13_btn_2)
screen_13_btn_2_label.set_text("")
screen_13_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_13_btn_2_label.set_width(lv.pct(100))
screen_13_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_13_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_13_btn_2.set_pos(32, 400)
screen_13_btn_2.set_size(49, 48)
# Set style for screen_13_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_13_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_13_btn_1
screen_13_btn_1 = lv.button(screen_13)
screen_13_btn_1_label = lv.label(screen_13_btn_1)
screen_13_btn_1_label.set_text("")
screen_13_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_13_btn_1_label.set_width(lv.pct(100))
screen_13_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_13_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_13_btn_1.set_pos(94, 400)
screen_13_btn_1.set_size(49, 48)
# Set style for screen_13_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_13_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_13_btn_5
screen_13_btn_5 = lv.button(screen_13)
screen_13_btn_5_label = lv.label(screen_13_btn_5)
screen_13_btn_5_label.set_text("")
screen_13_btn_5_label.set_long_mode(lv.label.LONG.WRAP)
screen_13_btn_5_label.set_width(lv.pct(100))
screen_13_btn_5_label.align(lv.ALIGN.CENTER, 0, 0)
screen_13_btn_5.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_13_btn_5.set_pos(285, 400)
screen_13_btn_5.set_size(229, 48)
# Set style for screen_13_btn_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_13_btn_5.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_5.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_5.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_5.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_5.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_5.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_5.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_13_btn_6
screen_13_btn_6 = lv.button(screen_13)
screen_13_btn_6_label = lv.label(screen_13_btn_6)
screen_13_btn_6_label.set_text("")
screen_13_btn_6_label.set_long_mode(lv.label.LONG.WRAP)
screen_13_btn_6_label.set_width(lv.pct(100))
screen_13_btn_6_label.align(lv.ALIGN.CENTER, 0, 0)
screen_13_btn_6.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_13_btn_6.set_pos(32, 126)
screen_13_btn_6.set_size(735, 238)
# Set style for screen_13_btn_6, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_13_btn_6.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_6.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_6.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_6.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_6.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_6.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_6.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_13_btn_6.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_13.update_layout()
# Create screen_14
screen_14 = lv.obj()
screen_14.set_size(800, 480)
screen_14.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_14, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_14.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_14_img_1
screen_14_img_1 = lv.image(screen_14)
screen_14_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\15_sarj_ozeti_ac_5_800_480.png"))
screen_14_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_14_img_1.set_pivot(50,50)
screen_14_img_1.set_rotation(0)
screen_14_img_1.set_pos(0, 0)
screen_14_img_1.set_size(800, 480)
# Set style for screen_14_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_14_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_14_btn_4
screen_14_btn_4 = lv.button(screen_14)
screen_14_btn_4_label = lv.label(screen_14_btn_4)
screen_14_btn_4_label.set_text("")
screen_14_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_14_btn_4_label.set_width(lv.pct(100))
screen_14_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_14_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_14_btn_4.set_pos(215, 400)
screen_14_btn_4.set_size(49, 48)
# Set style for screen_14_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_14_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_14_btn_3
screen_14_btn_3 = lv.button(screen_14)
screen_14_btn_3_label = lv.label(screen_14_btn_3)
screen_14_btn_3_label.set_text("")
screen_14_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_14_btn_3_label.set_width(lv.pct(100))
screen_14_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_14_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_14_btn_3.set_pos(154, 400)
screen_14_btn_3.set_size(49, 48)
# Set style for screen_14_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_14_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_14_btn_2
screen_14_btn_2 = lv.button(screen_14)
screen_14_btn_2_label = lv.label(screen_14_btn_2)
screen_14_btn_2_label.set_text("")
screen_14_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_14_btn_2_label.set_width(lv.pct(100))
screen_14_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_14_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_14_btn_2.set_pos(32, 400)
screen_14_btn_2.set_size(49, 48)
# Set style for screen_14_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_14_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_14_btn_1
screen_14_btn_1 = lv.button(screen_14)
screen_14_btn_1_label = lv.label(screen_14_btn_1)
screen_14_btn_1_label.set_text("")
screen_14_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_14_btn_1_label.set_width(lv.pct(100))
screen_14_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_14_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_14_btn_1.set_pos(94, 400)
screen_14_btn_1.set_size(49, 48)
# Set style for screen_14_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_14_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_14_btn_5
screen_14_btn_5 = lv.button(screen_14)
screen_14_btn_5_label = lv.label(screen_14_btn_5)
screen_14_btn_5_label.set_text("")
screen_14_btn_5_label.set_long_mode(lv.label.LONG.WRAP)
screen_14_btn_5_label.set_width(lv.pct(100))
screen_14_btn_5_label.align(lv.ALIGN.CENTER, 0, 0)
screen_14_btn_5.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_14_btn_5.set_pos(32, 116)
screen_14_btn_5.set_size(49, 48)
# Set style for screen_14_btn_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_14_btn_5.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_5.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_5.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_5.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_5.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_5.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_5.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_14_btn_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_14.update_layout()
# Create screen_15
screen_15 = lv.obj()
screen_15.set_size(800, 480)
screen_15.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_15, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_15.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_15_img_1
screen_15_img_1 = lv.image(screen_15)
screen_15_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\16_sarj_detaylari_ac_5_800_480.png"))
screen_15_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_15_img_1.set_pivot(50,50)
screen_15_img_1.set_rotation(0)
screen_15_img_1.set_pos(0, 0)
screen_15_img_1.set_size(800, 480)
# Set style for screen_15_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_15_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_15_btn_4
screen_15_btn_4 = lv.button(screen_15)
screen_15_btn_4_label = lv.label(screen_15_btn_4)
screen_15_btn_4_label.set_text("")
screen_15_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_15_btn_4_label.set_width(lv.pct(100))
screen_15_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_15_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_15_btn_4.set_pos(215, 400)
screen_15_btn_4.set_size(49, 48)
# Set style for screen_15_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_15_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_15_btn_3
screen_15_btn_3 = lv.button(screen_15)
screen_15_btn_3_label = lv.label(screen_15_btn_3)
screen_15_btn_3_label.set_text("")
screen_15_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_15_btn_3_label.set_width(lv.pct(100))
screen_15_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_15_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_15_btn_3.set_pos(154, 400)
screen_15_btn_3.set_size(49, 48)
# Set style for screen_15_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_15_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_15_btn_2
screen_15_btn_2 = lv.button(screen_15)
screen_15_btn_2_label = lv.label(screen_15_btn_2)
screen_15_btn_2_label.set_text("")
screen_15_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_15_btn_2_label.set_width(lv.pct(100))
screen_15_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_15_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_15_btn_2.set_pos(32, 400)
screen_15_btn_2.set_size(49, 48)
# Set style for screen_15_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_15_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_15_btn_1
screen_15_btn_1 = lv.button(screen_15)
screen_15_btn_1_label = lv.label(screen_15_btn_1)
screen_15_btn_1_label.set_text("")
screen_15_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_15_btn_1_label.set_width(lv.pct(100))
screen_15_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_15_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_15_btn_1.set_pos(94, 400)
screen_15_btn_1.set_size(49, 48)
# Set style for screen_15_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_15_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_15_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_15.update_layout()
# Create screen_16
screen_16 = lv.obj()
screen_16.set_size(800, 480)
screen_16.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_16, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_16.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_16_img_1
screen_16_img_1 = lv.image(screen_16)
screen_16_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\17_bilgilendirme_ac_5_800_480.png"))
screen_16_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_16_img_1.set_pivot(50,50)
screen_16_img_1.set_rotation(0)
screen_16_img_1.set_pos(0, 0)
screen_16_img_1.set_size(800, 480)
# Set style for screen_16_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_16_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_16_btn_4
screen_16_btn_4 = lv.button(screen_16)
screen_16_btn_4_label = lv.label(screen_16_btn_4)
screen_16_btn_4_label.set_text("")
screen_16_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_16_btn_4_label.set_width(lv.pct(100))
screen_16_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_16_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_16_btn_4.set_pos(215, 400)
screen_16_btn_4.set_size(49, 48)
# Set style for screen_16_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_16_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_16_btn_3
screen_16_btn_3 = lv.button(screen_16)
screen_16_btn_3_label = lv.label(screen_16_btn_3)
screen_16_btn_3_label.set_text("")
screen_16_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_16_btn_3_label.set_width(lv.pct(100))
screen_16_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_16_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_16_btn_3.set_pos(154, 400)
screen_16_btn_3.set_size(49, 48)
# Set style for screen_16_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_16_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_16_btn_2
screen_16_btn_2 = lv.button(screen_16)
screen_16_btn_2_label = lv.label(screen_16_btn_2)
screen_16_btn_2_label.set_text("")
screen_16_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_16_btn_2_label.set_width(lv.pct(100))
screen_16_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_16_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_16_btn_2.set_pos(32, 400)
screen_16_btn_2.set_size(49, 48)
# Set style for screen_16_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_16_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_16_btn_1
screen_16_btn_1 = lv.button(screen_16)
screen_16_btn_1_label = lv.label(screen_16_btn_1)
screen_16_btn_1_label.set_text("")
screen_16_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_16_btn_1_label.set_width(lv.pct(100))
screen_16_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_16_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_16_btn_1.set_pos(94, 400)
screen_16_btn_1.set_size(49, 48)
# Set style for screen_16_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_16_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_16_btn_5
screen_16_btn_5 = lv.button(screen_16)
screen_16_btn_5_label = lv.label(screen_16_btn_5)
screen_16_btn_5_label.set_text("")
screen_16_btn_5_label.set_long_mode(lv.label.LONG.WRAP)
screen_16_btn_5_label.set_width(lv.pct(100))
screen_16_btn_5_label.align(lv.ALIGN.CENTER, 0, 0)
screen_16_btn_5.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_16_btn_5.set_pos(32, 32)
screen_16_btn_5.set_size(49, 48)
# Set style for screen_16_btn_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_16_btn_5.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_5.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_5.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_5.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_5.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_5.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_5.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_16_btn_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_16.update_layout()
# Create screen_17
screen_17 = lv.obj()
screen_17.set_size(800, 480)
screen_17.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_17, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_17.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_17_img_1
screen_17_img_1 = lv.image(screen_17)
screen_17_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\18_nasil_sarj_ederim_ac_5_800_480.png"))
screen_17_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_17_img_1.set_pivot(50,50)
screen_17_img_1.set_rotation(0)
screen_17_img_1.set_pos(0, 0)
screen_17_img_1.set_size(800, 480)
# Set style for screen_17_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_17_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_17_btn_4
screen_17_btn_4 = lv.button(screen_17)
screen_17_btn_4_label = lv.label(screen_17_btn_4)
screen_17_btn_4_label.set_text("")
screen_17_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_17_btn_4_label.set_width(lv.pct(100))
screen_17_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_17_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_17_btn_4.set_pos(215, 400)
screen_17_btn_4.set_size(49, 48)
# Set style for screen_17_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_17_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_17_btn_3
screen_17_btn_3 = lv.button(screen_17)
screen_17_btn_3_label = lv.label(screen_17_btn_3)
screen_17_btn_3_label.set_text("")
screen_17_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_17_btn_3_label.set_width(lv.pct(100))
screen_17_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_17_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_17_btn_3.set_pos(154, 400)
screen_17_btn_3.set_size(49, 48)
# Set style for screen_17_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_17_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_17_btn_2
screen_17_btn_2 = lv.button(screen_17)
screen_17_btn_2_label = lv.label(screen_17_btn_2)
screen_17_btn_2_label.set_text("")
screen_17_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_17_btn_2_label.set_width(lv.pct(100))
screen_17_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_17_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_17_btn_2.set_pos(32, 400)
screen_17_btn_2.set_size(49, 48)
# Set style for screen_17_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_17_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_17_btn_1
screen_17_btn_1 = lv.button(screen_17)
screen_17_btn_1_label = lv.label(screen_17_btn_1)
screen_17_btn_1_label.set_text("")
screen_17_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_17_btn_1_label.set_width(lv.pct(100))
screen_17_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_17_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_17_btn_1.set_pos(94, 400)
screen_17_btn_1.set_size(49, 48)
# Set style for screen_17_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_17_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_17_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_17.update_layout()
# Create screen_18
screen_18 = lv.obj()
screen_18.set_size(800, 480)
screen_18.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_18, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_18.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_18_img_1
screen_18_img_1 = lv.image(screen_18)
screen_18_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\19_rfid_kart_ile_sarj_ac_5_800_480.png"))
screen_18_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_18_img_1.set_pivot(50,50)
screen_18_img_1.set_rotation(0)
screen_18_img_1.set_pos(0, 0)
screen_18_img_1.set_size(800, 480)
# Set style for screen_18_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_18_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_18_btn_4
screen_18_btn_4 = lv.button(screen_18)
screen_18_btn_4_label = lv.label(screen_18_btn_4)
screen_18_btn_4_label.set_text("")
screen_18_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_18_btn_4_label.set_width(lv.pct(100))
screen_18_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_18_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_18_btn_4.set_pos(215, 400)
screen_18_btn_4.set_size(49, 48)
# Set style for screen_18_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_18_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_18_btn_3
screen_18_btn_3 = lv.button(screen_18)
screen_18_btn_3_label = lv.label(screen_18_btn_3)
screen_18_btn_3_label.set_text("")
screen_18_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_18_btn_3_label.set_width(lv.pct(100))
screen_18_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_18_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_18_btn_3.set_pos(154, 400)
screen_18_btn_3.set_size(49, 48)
# Set style for screen_18_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_18_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_18_btn_2
screen_18_btn_2 = lv.button(screen_18)
screen_18_btn_2_label = lv.label(screen_18_btn_2)
screen_18_btn_2_label.set_text("")
screen_18_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_18_btn_2_label.set_width(lv.pct(100))
screen_18_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_18_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_18_btn_2.set_pos(32, 400)
screen_18_btn_2.set_size(49, 48)
# Set style for screen_18_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_18_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_18_btn_1
screen_18_btn_1 = lv.button(screen_18)
screen_18_btn_1_label = lv.label(screen_18_btn_1)
screen_18_btn_1_label.set_text("")
screen_18_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_18_btn_1_label.set_width(lv.pct(100))
screen_18_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_18_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_18_btn_1.set_pos(94, 400)
screen_18_btn_1.set_size(49, 48)
# Set style for screen_18_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_18_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_18_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_18.update_layout()
# Create screen_19
screen_19 = lv.obj()
screen_19.set_size(800, 480)
screen_19.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_19, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_19.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_19_img_1
screen_19_img_1 = lv.image(screen_19)
screen_19_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\20_mobil_uygulama_ile_sarj_ac_5_800_480.png"))
screen_19_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_19_img_1.set_pivot(50,50)
screen_19_img_1.set_rotation(0)
screen_19_img_1.set_pos(0, 0)
screen_19_img_1.set_size(800, 480)
# Set style for screen_19_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_19_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_19_btn_4
screen_19_btn_4 = lv.button(screen_19)
screen_19_btn_4_label = lv.label(screen_19_btn_4)
screen_19_btn_4_label.set_text("")
screen_19_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_19_btn_4_label.set_width(lv.pct(100))
screen_19_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_19_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_19_btn_4.set_pos(215, 400)
screen_19_btn_4.set_size(49, 48)
# Set style for screen_19_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_19_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_19_btn_3
screen_19_btn_3 = lv.button(screen_19)
screen_19_btn_3_label = lv.label(screen_19_btn_3)
screen_19_btn_3_label.set_text("")
screen_19_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_19_btn_3_label.set_width(lv.pct(100))
screen_19_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_19_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_19_btn_3.set_pos(154, 400)
screen_19_btn_3.set_size(49, 48)
# Set style for screen_19_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_19_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_19_btn_2
screen_19_btn_2 = lv.button(screen_19)
screen_19_btn_2_label = lv.label(screen_19_btn_2)
screen_19_btn_2_label.set_text("")
screen_19_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_19_btn_2_label.set_width(lv.pct(100))
screen_19_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_19_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_19_btn_2.set_pos(32, 400)
screen_19_btn_2.set_size(49, 48)
# Set style for screen_19_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_19_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_19_btn_1
screen_19_btn_1 = lv.button(screen_19)
screen_19_btn_1_label = lv.label(screen_19_btn_1)
screen_19_btn_1_label.set_text("")
screen_19_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_19_btn_1_label.set_width(lv.pct(100))
screen_19_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_19_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_19_btn_1.set_pos(94, 400)
screen_19_btn_1.set_size(49, 48)
# Set style for screen_19_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_19_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_19_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_19.update_layout()
# Create screen_20
screen_20 = lv.obj()
screen_20.set_size(800, 480)
screen_20.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_20, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_20.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_20_img_1
screen_20_img_1 = lv.image(screen_20)
screen_20_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\21_dil_secimi_ac_5_800_480.png"))
screen_20_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_20_img_1.set_pivot(50,50)
screen_20_img_1.set_rotation(0)
screen_20_img_1.set_pos(0, 0)
screen_20_img_1.set_size(800, 480)
# Set style for screen_20_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_20_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_20_btn_4
screen_20_btn_4 = lv.button(screen_20)
screen_20_btn_4_label = lv.label(screen_20_btn_4)
screen_20_btn_4_label.set_text("")
screen_20_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_20_btn_4_label.set_width(lv.pct(100))
screen_20_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_20_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_20_btn_4.set_pos(215, 400)
screen_20_btn_4.set_size(49, 48)
# Set style for screen_20_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_20_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_20_btn_3
screen_20_btn_3 = lv.button(screen_20)
screen_20_btn_3_label = lv.label(screen_20_btn_3)
screen_20_btn_3_label.set_text("")
screen_20_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_20_btn_3_label.set_width(lv.pct(100))
screen_20_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_20_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_20_btn_3.set_pos(154, 400)
screen_20_btn_3.set_size(49, 48)
# Set style for screen_20_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_20_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_20_btn_2
screen_20_btn_2 = lv.button(screen_20)
screen_20_btn_2_label = lv.label(screen_20_btn_2)
screen_20_btn_2_label.set_text("")
screen_20_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_20_btn_2_label.set_width(lv.pct(100))
screen_20_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_20_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_20_btn_2.set_pos(32, 400)
screen_20_btn_2.set_size(49, 48)
# Set style for screen_20_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_20_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_20_btn_1
screen_20_btn_1 = lv.button(screen_20)
screen_20_btn_1_label = lv.label(screen_20_btn_1)
screen_20_btn_1_label.set_text("")
screen_20_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_20_btn_1_label.set_width(lv.pct(100))
screen_20_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_20_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_20_btn_1.set_pos(94, 400)
screen_20_btn_1.set_size(49, 48)
# Set style for screen_20_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_20_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_20_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_20.update_layout()
# Create screen_21
screen_21 = lv.obj()
screen_21.set_size(800, 480)
screen_21.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_21, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_21.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_21_img_1
screen_21_img_1 = lv.image(screen_21)
screen_21_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\22_ayarlar_giris_ac_5_800_480.png"))
screen_21_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_21_img_1.set_pivot(50,50)
screen_21_img_1.set_rotation(0)
screen_21_img_1.set_pos(0, -1)
screen_21_img_1.set_size(800, 480)
# Set style for screen_21_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_21_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_21_btn_4
screen_21_btn_4 = lv.button(screen_21)
screen_21_btn_4_label = lv.label(screen_21_btn_4)
screen_21_btn_4_label.set_text("")
screen_21_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_21_btn_4_label.set_width(lv.pct(100))
screen_21_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_21_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_21_btn_4.set_pos(215, 400)
screen_21_btn_4.set_size(49, 48)
# Set style for screen_21_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_21_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_21_btn_3
screen_21_btn_3 = lv.button(screen_21)
screen_21_btn_3_label = lv.label(screen_21_btn_3)
screen_21_btn_3_label.set_text("")
screen_21_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_21_btn_3_label.set_width(lv.pct(100))
screen_21_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_21_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_21_btn_3.set_pos(154, 400)
screen_21_btn_3.set_size(49, 48)
# Set style for screen_21_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_21_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_21_btn_2
screen_21_btn_2 = lv.button(screen_21)
screen_21_btn_2_label = lv.label(screen_21_btn_2)
screen_21_btn_2_label.set_text("")
screen_21_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_21_btn_2_label.set_width(lv.pct(100))
screen_21_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_21_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_21_btn_2.set_pos(32, 400)
screen_21_btn_2.set_size(49, 48)
# Set style for screen_21_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_21_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_21_btn_1
screen_21_btn_1 = lv.button(screen_21)
screen_21_btn_1_label = lv.label(screen_21_btn_1)
screen_21_btn_1_label.set_text("")
screen_21_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_21_btn_1_label.set_width(lv.pct(100))
screen_21_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_21_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_21_btn_1.set_pos(94, 400)
screen_21_btn_1.set_size(49, 48)
# Set style for screen_21_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_21_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_21_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_21.update_layout()
# Create screen_22
screen_22 = lv.obj()
screen_22.set_size(800, 480)
screen_22.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_22, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_22.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_22_img_1
screen_22_img_1 = lv.image(screen_22)
screen_22_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\23_ayarlar_ac_5_800_480.png"))
screen_22_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_22_img_1.set_pivot(50,50)
screen_22_img_1.set_rotation(0)
screen_22_img_1.set_pos(0, 0)
screen_22_img_1.set_size(800, 480)
# Set style for screen_22_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_22_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_22_btn_4
screen_22_btn_4 = lv.button(screen_22)
screen_22_btn_4_label = lv.label(screen_22_btn_4)
screen_22_btn_4_label.set_text("")
screen_22_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_22_btn_4_label.set_width(lv.pct(100))
screen_22_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_22_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_22_btn_4.set_pos(215, 400)
screen_22_btn_4.set_size(49, 48)
# Set style for screen_22_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_22_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_22_btn_3
screen_22_btn_3 = lv.button(screen_22)
screen_22_btn_3_label = lv.label(screen_22_btn_3)
screen_22_btn_3_label.set_text("")
screen_22_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_22_btn_3_label.set_width(lv.pct(100))
screen_22_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_22_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_22_btn_3.set_pos(154, 400)
screen_22_btn_3.set_size(49, 48)
# Set style for screen_22_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_22_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_22_btn_2
screen_22_btn_2 = lv.button(screen_22)
screen_22_btn_2_label = lv.label(screen_22_btn_2)
screen_22_btn_2_label.set_text("")
screen_22_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_22_btn_2_label.set_width(lv.pct(100))
screen_22_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_22_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_22_btn_2.set_pos(32, 400)
screen_22_btn_2.set_size(49, 48)
# Set style for screen_22_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_22_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_22_btn_1
screen_22_btn_1 = lv.button(screen_22)
screen_22_btn_1_label = lv.label(screen_22_btn_1)
screen_22_btn_1_label.set_text("")
screen_22_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_22_btn_1_label.set_width(lv.pct(100))
screen_22_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_22_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_22_btn_1.set_pos(94, 400)
screen_22_btn_1.set_size(49, 48)
# Set style for screen_22_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_22_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_22_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_22.update_layout()
# Create screen_23
screen_23 = lv.obj()
screen_23.set_size(800, 480)
screen_23.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_23, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_23.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_23_img_1
screen_23_img_1 = lv.image(screen_23)
screen_23_img_1.set_src(load_image(r"C:\NXP\GUI-Guider-Projects\zebradark800480\generated\MicroPython\24_ag_ayarlari_ac_5_800_480.png"))
screen_23_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
screen_23_img_1.set_pivot(50,50)
screen_23_img_1.set_rotation(0)
screen_23_img_1.set_pos(0, 0)
screen_23_img_1.set_size(800, 480)
# Set style for screen_23_img_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_23_img_1.set_style_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_23_btn_4
screen_23_btn_4 = lv.button(screen_23)
screen_23_btn_4_label = lv.label(screen_23_btn_4)
screen_23_btn_4_label.set_text("")
screen_23_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_23_btn_4_label.set_width(lv.pct(100))
screen_23_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_23_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_23_btn_4.set_pos(215, 400)
screen_23_btn_4.set_size(49, 48)
# Set style for screen_23_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_23_btn_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_23_btn_3
screen_23_btn_3 = lv.button(screen_23)
screen_23_btn_3_label = lv.label(screen_23_btn_3)
screen_23_btn_3_label.set_text("")
screen_23_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_23_btn_3_label.set_width(lv.pct(100))
screen_23_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_23_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_23_btn_3.set_pos(154, 400)
screen_23_btn_3.set_size(49, 48)
# Set style for screen_23_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_23_btn_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_23_btn_2
screen_23_btn_2 = lv.button(screen_23)
screen_23_btn_2_label = lv.label(screen_23_btn_2)
screen_23_btn_2_label.set_text("")
screen_23_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_23_btn_2_label.set_width(lv.pct(100))
screen_23_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_23_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_23_btn_2.set_pos(32, 400)
screen_23_btn_2.set_size(49, 48)
# Set style for screen_23_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_23_btn_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_23_btn_1
screen_23_btn_1 = lv.button(screen_23)
screen_23_btn_1_label = lv.label(screen_23_btn_1)
screen_23_btn_1_label.set_text("")
screen_23_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_23_btn_1_label.set_width(lv.pct(100))
screen_23_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_23_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_23_btn_1.set_pos(94, 400)
screen_23_btn_1.set_size(49, 48)
# Set style for screen_23_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_23_btn_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_23_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_23.update_layout()

def screen_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.SCREEN_LOAD_START):
        pass
        lv.screen_load_anim(screen_1, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen.add_event_cb(lambda e: screen_event_handler(e), lv.EVENT.ALL, None)

def screen_1_btn_1_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_17, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_1_btn_1.add_event_cb(lambda e: screen_1_btn_1_event_handler(e), lv.EVENT.ALL, None)

def screen_1_btn_2_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_2, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_1_btn_2.add_event_cb(lambda e: screen_1_btn_2_event_handler(e), lv.EVENT.ALL, None)

def screen_1_btn_3_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_3, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_1_btn_3.add_event_cb(lambda e: screen_1_btn_3_event_handler(e), lv.EVENT.ALL, None)

def screen_1_btn_4_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_4, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_1_btn_4.add_event_cb(lambda e: screen_1_btn_4_event_handler(e), lv.EVENT.ALL, None)

def screen_1_btn_9_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_5, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_1_btn_9.add_event_cb(lambda e: screen_1_btn_9_event_handler(e), lv.EVENT.ALL, None)

def screen_5_btn_5_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_6, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_5_btn_5.add_event_cb(lambda e: screen_5_btn_5_event_handler(e), lv.EVENT.ALL, None)

def screen_6_btn_1_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_8, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_6_btn_1.add_event_cb(lambda e: screen_6_btn_1_event_handler(e), lv.EVENT.ALL, None)

def screen_8_btn_5_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_13, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_8_btn_5.add_event_cb(lambda e: screen_8_btn_5_event_handler(e), lv.EVENT.ALL, None)

def screen_9_btn_5_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_13, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_9_btn_5.add_event_cb(lambda e: screen_9_btn_5_event_handler(e), lv.EVENT.ALL, None)

def screen_13_btn_6_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_14, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_13_btn_6.add_event_cb(lambda e: screen_13_btn_6_event_handler(e), lv.EVENT.ALL, None)

def screen_14_btn_5_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_15, lv.SCR_LOAD_ANIM.NONE, 200, 200, False)
screen_14_btn_5.add_event_cb(lambda e: screen_14_btn_5_event_handler(e), lv.EVENT.ALL, None)

def screen_16_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
screen_16.add_event_cb(lambda e: screen_16_event_handler(e), lv.EVENT.ALL, None)

def screen_16_btn_5_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
screen_16_btn_5.add_event_cb(lambda e: screen_16_btn_5_event_handler(e), lv.EVENT.ALL, None)

# content from custom.py

# Load the default screen
lv.screen_load(screen)

if __name__ == '__main__':
    while True:
        lv.task_handler()
        time.sleep_ms(5)
