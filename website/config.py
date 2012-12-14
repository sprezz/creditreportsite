# -*- coding:utf-8 -*-
from livesettings import config_register, ConfigurationGroup, BooleanValue


CONFIG_GROUP = ConfigurationGroup('website', 'Website settings')

config_register(BooleanValue(CONFIG_GROUP, 'ENABLE_ISP_FILTER', default=True))
