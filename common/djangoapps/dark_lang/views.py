"""
Views file for the Darklang Django App
"""
from openedx.core.lib.api.view_utils import view_auth_classes
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from edxmako.shortcuts import render_to_response

from openedx.core.djangoapps.user_api.preferences.api import (
    delete_user_preference, get_user_preference, set_user_preference
)
from lang_pref import LANGUAGE_KEY

from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils.translation import ugettext as _

from dark_lang import DARK_LANGUAGE_KEY
from dark_lang.models import DarkLangConfig

LANGUAGE_INPUT_FIELD = 'preview_lang'


@view_auth_classes()
class DarkLangView(View):
    """
    View used when a user is attempting to change the preview language using Darklang.

    Expected Behavior:
    GET - returns a form for setting/resetting the user's dark language
    POST - updates or clears the setting to the given dark language

    Note: This class and View are meant to replace the ability to set the DarkLang in the middleware, which was
    determined to be a security risk. (TNL-4742)
    """
    template_name = 'darklang/preview_lang.html'

    @method_decorator(login_required)
    def get(self, request):
        """
        Displays the Form for setting/resetting a User's dark language setting

        Arguments:
            request (Request): The Django Request Object

        Returns:
            HttpResponse: View containing the form for setting the preview lang
        """
        context = {
            'disable_courseware_js': True,
            'uses_pattern_library': True
        }
        return render_to_response(self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        """
        Sets or clears the DarkLang depending on the incoming post data.

        Arguments:
            request (Request): The Django Request Object

        Returns:
            HttpResponse: View containing the form for setting the preview lang
        """
        context = {
            'disable_courseware_js': True,
            'uses_pattern_library': True
        }
        (success, result) = self.process_darklang_request(request)
        if result is not None:
            context.update({'form_submit_message': result})
            context.update({'success': success})
        return render_to_response(self.template_name, context)

    def process_darklang_request(self, request):
        """
        Prevent user from requesting un-released languages
        """
        if not DarkLangConfig.current().enabled:
            return False, _('Preview Language is currently disabled')

        success = False
        result = None
        if 'reset' in request.POST:
            # Reset and clear the language preference
            (success, result) = self._clear_preview_language(request)
        if 'set_language' in request.POST:
            # Set the Preview Language
            (success, result) = self._set_preview_language(request)
        return success, result

    def _set_preview_language(self, request):
        """
        Attempt to set the Preview language

        Arguments:
            request (Request): The incoming Django Request

        Returns:
            bool: True for successful setting of the language code
            str: The response message to be presented
        """
        if LANGUAGE_INPUT_FIELD not in request.POST:
            return False, _('Language code not provided')

        preview_lang = request.POST[LANGUAGE_INPUT_FIELD]

        if preview_lang == '':
            return False, _('Language code not provided')

        auth_user = request.user.is_authenticated()

        # Set the session key to the requested preview lang
        request.session[LANGUAGE_SESSION_KEY] = preview_lang

        # Make sure that we set the requested preview lang as the dark lang preference for the
        # user, so that the lang_pref middleware doesn't clobber away the dark lang preview.
        if auth_user:
            set_user_preference(request.user, DARK_LANGUAGE_KEY, preview_lang)
        return True, _('Language set to language code: {preview_language_code}').format(
            preview_language_code=preview_lang)

    def _clear_preview_language(self, request):
        """
        Clears the dark language preview

        Arguments:
            request (Request): The incoming Django Request

        Returns:
            bool: True for successful clearing of the language code
            str: The response message to be presented
        """
        auth_user = request.user.is_authenticated()

        # delete the session language key (if one is set)
        if LANGUAGE_SESSION_KEY in request.session:
            del request.session[LANGUAGE_SESSION_KEY]

        user_pref = ''
        if auth_user:
            # Reset user's dark lang preference to null
            delete_user_preference(request.user, DARK_LANGUAGE_KEY)
            # Get & set user's preferred language
            user_pref = get_user_preference(request.user, LANGUAGE_KEY)
            if user_pref:
                request.session[LANGUAGE_SESSION_KEY] = user_pref
        if user_pref is None:
            return True, _('Language reset to the default language code')
        return True, _("Language reset to user's preference: {preview_language_code}").format(
            preview_language_code=user_pref)
