from flask import Blueprint, redirect

placeholders = Blueprint("placeholders", __name__)

@placeholders.route("/placekitten/<height>/<width>")
def placekitten(height, width):
    '''    __..--''``---....___   _..._    __
 /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
///_.-' _..--.'_    \                    `( ) ) // //
/ (_..-' // (< _     ;_..__               ; `' / ///
 / // // //  `-._,_)' // / ``--...____..-' /// / //

    Enjoy the next 45 minutes
    '''
    return redirect("http://placekitten.com/{}/{}".format(height, width))

@placeholders.route("/placepuppy/<height>/<width>")
def placedog(height, width):
#                 .--~~,__
#:-....,-------`~~'._.'
# `-,,,  ,_      ;'~U'
#  _,-' ,'`-__; '--.
# (_/'~~      ''''(;

#    Enjoy the next 45 minutes (again)
    return redirect("http://place-puppy.com/{}/{}".format(height, width))

@placeholders.route("/httpcat/<status>")
def httpcat(status):
    '''    __..--''``---....___   _..._    __
 /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
///_.-' _..--.'_    \                    `( ) ) // //
/ (_..-' // (< _     ;_..__               ; `' / ///
 / // // //  `-._,_)' // / ``--...____..-' /// / //

    Enjoy the next 45 minutes
    '''
    return redirect("http://http.cat/{}".format(status))

@placeholders.route("/cataas")
def cataas():
    '''       __..--''``---....___   _..._    __
    /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
    ///_.-' _..--.'_    \                    `( ) ) // //
    / (_..-' // (< _     ;_..__               ; `' / ///
    / // // //  `-._,_)' // / ``--...____..-' /// / //

    Enjoy the next 45 minutes
    '''
    return redirect("https://cataas.com/cat")

@placeholders.route("/cataas/gif")
def cataas_gif():
    '''
    no more cat ascii art :(
    '''
    return redirect("https://cataas.com/cat/gif")

@placeholders.route("/cataas/<tag>")
def cataas_tag(tag):
    return redirect("https://cataas.com/cat/{}".format(tag))

@placeholders.route("/cataas/gif/<tag>")
def cataas_gif_tag(tag):
    return redirect("https://cataas.com/cat/gif/{}".format(tag))
