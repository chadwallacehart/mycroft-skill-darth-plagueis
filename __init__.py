# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import adds_context, removes_context
from mycroft.skills.core import FallbackSkill
from mycroft.util.log import LOG
from mycroft.util import play_wav as play
from time import sleep
import os
import sys

skill_path = "/opt/mycroft/skills/skill-darth-plagueis/"
sys.path.append(skill_path)
import led # for led control on the aiy voice kit

# This was my first test based on the default skill template
# See the 2nd class below for more sophisticated dialog control
# ToDo: delete
class PlagueisSkillBasic(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(PlagueisSkillBasic, self).__init__(name="PlagueisSkill")

        self.finished = False

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of thewhat files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    @intent_handler(IntentBuilder("").require("Darth_Plagueis"))
    def handle_darth_plagueis_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog

        def no_response():
            self.speak_dialog("tragedy5")
            finished = True
            return

        choice = self.get_response('tragedy1')
        if not choice:
            no_response()
        else:
            choice = self.get_response('tragedy2')
            if not choice:
                no_response()
            else:
                choice = self.get_response('tragedy3')
                if not choice:
                    no_response()
                else:
                    choice = self.get_response('tragedy4')
                    if not choice:
                        no_response()
                    else:
                        self.speak_dialog("tragedy5")


        self.finished = True

    # look at converse



# The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    def stop(self):
        if self.finished is False:
            self.speak_dialog("tragedy5")
        return True


class PlagueisSkillContext(MycroftSkill):
    def __init__(self, mode='tts'):
        super(PlagueisSkillContext, self).__init__(name='PlagueisSkill')
        self.darkside = False
        self.started = False
        if mode=='wav':
            self.wav_mode = True
        else:
            self.wav_mode = False

        LOG("PlagueisSKill").debug("Darth Plagueis skill loaded")

    def story(self):
        if self.wav_mode:
            play(os.path.join(skill_path,'audio/tragedy of darth plagueis 2.wav'))
            led.wait(35)
            self.speak(" ", expect_response=True)
        else:
            self.speak("I thought not.")
            self.speak("It's not a story the Jedi would tell you.")
            self.speak("It's a Sith legend.")
            self.speak("Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force "
                       "to influence the midichlorians to create life...")
            self.speak("He had such a knowledge of the dark side that he could even keep the ones he cared about "
                       "from dying.", expect_response=True)


    @intent_handler(IntentBuilder('DarthPlagueis').require('Darth_Plagueis'))
    @adds_context('PlagueisContext')
    def handle_darth_plagueis_intent(self, message):
        self.started = True

        # choice = self.get_response("Did you ever hear the tragedy of Darth Plagueis the Wise?")
        if self.wav_mode:
            play(os.path.join(skill_path,'audio/tragedy of darth plagueis 1.wav'))
            led.wait(5)
            self.speak(" ", expect_response=True)

        else:
            self.speak("Did you ever hear the tragedy of Darth Plagueis the Wise?")

        # ToDo: find a better way to move to the next line if there is no response
        # the blank dialog below does not work with the Google TTS, so removed
        '''
        response = self.get_response('blank')

        if response == "yes" or response == "yeah":
            self.speak("Not from a Jedi")
            self.remove_context('PlagueisContext')
        else:
            self.story()
        '''

    # ToDo: set the 'yes' and 'no' below to only work after the initial "Did you ever hear.."
    @intent_handler(IntentBuilder("NotFamiliarIntent").require('no').require('PlagueisContext').build())
    def handle_not_familiar_intent(self, message):
        self.story()


    @intent_handler(IntentBuilder("FamiliarIntent").require('yes').require('PlagueisContext').build())
    @removes_context('PlagueisContext')
    def handle_familiar_intent(self, message):
        if self.wav_mode:
            play(os.path.join(skill_path,'audio/tragedy of darth plagueis 5.wav'))
            led.wait(1.2, led.LED.ON)
        else:
            self.speak("Not from a Jedi")


    @intent_handler(IntentBuilder('SaveFromDeathIntent').require('save_death').require('PlagueisContext').build())
    @adds_context('SaveFromDeathContext')
    def handle_save_from_death_intent(self, message):
        if self.wav_mode:
            play(os.path.join(skill_path,'audio/tragedy of darth plagueis 3.wav'))
            led.wait(8)
            self.speak(" ", expect_response=True)
        else:
            self.speak("The dark side of the Force is a pathway to many abilities some consider to be unnatural.", expect_response=True)

        self.darkside = True


    @intent_handler(IntentBuilder('WhatHappened').require('happened').require('PlagueisContext').build())
    @adds_context('SaveFromDeathContext')
    def what_happened_intent(self, message):
        if self.wav_mode:
            play(os.path.join(skill_path,'audio/tragedy of darth plagueis 4.wav'))
            led.wait(31)
            self.speak(" ", expect_response=True)
        else:
            self.speak("He became so powerful... "
                       "the only thing he was afraid of was losing his power, which eventually, of course, he did.")
            self.speak("Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep.")
            sleep(0.4)
            self.speak("It's ironic he could save others from death, but not himself.", expect_response=True)


    @intent_handler(IntentBuilder('LearnThisPower').require('learn')
                    .require('SaveFromDeathContext').require('PlagueisContext').build())
    @removes_context('PlagueisContext')
    @removes_context('SaveFromDeathContext')
    def handle_can_be_learned_intent(self, message):
        if self.wav_mode:
            play(os.path.join(skill_path,'audio/tragedy of darth plagueis 5.wav'))
            led.wait(1, led.LED.ON)
        else:
            self.speak("Not from a Jedi")


    @removes_context('PlagueisContext')
    @removes_context('SaveFromDeathContext')
    def stop(self):
        if self.started and not self.darkside:
                if self.wav_mode:
                    play(os.path.join(skill_path,'audio/tragedy of darth plagueis 3.wav'))
                    led.wait(8)

                else:
                    self.speak("The dark side of the Force is a pathway to many abilities some consider to be unnatural.")

        return True


def create_skill():
    return PlagueisSkillContext(mode='wav')
