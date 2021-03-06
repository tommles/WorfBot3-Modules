import operator

import willie

def setup(bot):
    if not bot.memory.contains('heretics'):
        bot.memory['heretics'] = willie.tools.WillieMemory()

@willie.module.rule(r'(\w+) is a(?:n)? heretic')
@willie.module.rule(r'(\w+) are heretics')
def denounce_heretic(bot, trigger):
    target = trigger.group(1)
    if target not in bot.memory['heretics']:
        init_heretic_target(bot, target)
    # Check for this user's judgment
    if trigger.nick in bot.memory['heretics'][target]['no']:
        # User has changed his mind; remove from list of "no"s
        bot.memory['heretics'][target]['no'].remove(trigger.nick)

    if trigger.nick not in bot.memory['heretics'][target]['yes']:
        # User has not denounced target before; add to list of "yes"s
        bot.memory['heretics'][target]['yes'].append(trigger.nick)
    bot.say('noted')

@willie.module.rule(r'(\w+) is not a(?:n)? heretic')
@willie.module.rule(r'(\w+) are not heretics')
def deny_heresy(bot, trigger):
    target = trigger.group(1)
    if target not in bot.memory['heretics']:
        init_heretic_target(bot, target)
    # Check for this user's judgment
    if trigger.nick in bot.memory['heretics'][target]['yes']:
        # User has changed his mind; remove from list of "yes"s
        bot.memory['heretics'][target]['yes'].remove(trigger.nick)

    if trigger.nick not in bot.memory['heretics'][target]['no']:
        # User has not denied target before; add to list of "no"s
        bot.memory['heretics'][target]['no'].append(trigger.nick)
    bot.say('noted')

def init_heretic_target(bot, target):
    bot.memory['heretics'][target] = { 'yes': [], 'no': [] }

def total_denunciations(target):
    return (target[0], len(target[1]['yes']) - len(target[1]['no']))

@willie.module.commands('heretics')
@willie.module.example('.heretics')
def heretics(bot, trigger):
    bot.say('Top Heretics')
    for i, heretic in enumerate([ x for x in sorted(map(total_denunciations, bot.memory['heretics'].iteritems()), key=operator.itemgetter(1), reverse=True) if x[1] > 0][:5]):
        bot.say('  #' + str(i + 1) + ' ' + heretic[0] + ' (' + str(heretic[1]) + ' denunciation' + ('s' if heretic[1] != 1 else '') + ')')

@willie.module.commands('heretic')
@willie.module.example('.heretic')
def heretic(bot, trigger):
    target = trigger.nick
    if trigger.group(2):
        target = trigger.group(2)

    if target in bot.memory['heretics']:
        obj = bot.memory['heretics'][target]
        total = len(obj['yes']) - len(obj['no'])
        bot.say(target + ' (' + str(total) + ' denunciation' + ('s' if total != 1 else '') + ')')
    else:
        bot.say(target + ' (0 denunciations)')
