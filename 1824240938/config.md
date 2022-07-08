<style>
    setting {
        background-color: #99999999;
        font-weight: bold;
    }

    key {
        background-color: #44999999;
    }

    version {
        font-weight: normal;
        font-size: medium;
    }
</style>

# Wallpaper <version>v1.0-0-ga0b83f4</version>

Note that in order to see the wallpaper while reviewing, 
you *must* remove the background color from your card CSS. 

Set <setting>&nbsp;`enabled_for`&nbsp;</setting> to a list of windows 
that will use wallpapers. You can use a combination of: 
<key>&nbsp;`main_window`&nbsp;</key>, 
<key>&nbsp;`add_cards`&nbsp;</key>, 
<key>&nbsp;`edit_current`&nbsp;</key>, 
<key>&nbsp;`edit`&nbsp;</key>, 
<key>&nbsp;`previewer`&nbsp;</key>.

Set <setting>&nbsp;`folder_with_wallpapers`&nbsp;</setting> 
to the full path of the folder containing your wallpaper images. 
Path will be separated either by forward slashes, 
or by double backwards slashes, for example:

* `/home/user/anki-wallpapers`
* `C:\\Users\\user\\anki-wallpapers\\`

The folder should have at least one wallpaper for the light mode,
and at least one for the dark mode.
Dark mode wallpapers will have <key>&nbsp;`dark`&nbsp;</key> in their name, 
separated from other parts of the name using the characters 
<key>&nbsp;`-`&nbsp;</key>, 
<key>&nbsp;`_`&nbsp;</key>, 
<key>&nbsp;`.`&nbsp;</key> or 
<key>&nbsp;&nbsp;&nbsp;</key> (space).

By default, wallpapers will be anchored by the centre, 
that is, the center of the wallpaper will be in the center of the window.
You can change anchoring by putting a combination of the following in the file name: 
<key>&nbsp;`center`&nbsp;</key>, 
<key>&nbsp;`top`&nbsp;</key>, 
<key>&nbsp;`left`&nbsp;</key>, 
<key>&nbsp;`bottom`&nbsp;</key>, 
<key>&nbsp;`right`&nbsp;</key>.
Some examples:

* `clouds.jpg`: light mode, center-anchored;
* `snow.bottom.left.jpg`: light mode, bottom-left-anchored;
* `gloomy_mountains-dark-top.jpeg`: dark mode, top-anchored.

The configuration takes effect immediately.