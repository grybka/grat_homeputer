"""Demo platform that offers fake air quality data."""
from homeassistant.components.air_quality import AirQualityEntity
from dripline.core import Service, message,constants
import logging
logger = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Air Quality."""
    print("config is {}".format(config))
    add_entities([
        GratAirQuality('Home', 14, 23, 100),
    ])

class GratAirQualityConnection(Service):
    """interface to dripline"""
    def __init__(self):
        Service.__init__(self,broker="10.0.0.4",exchange='requests',keys='#')

class GratAirQuality(AirQualityEntity):
    """Representation of Air Quality data."""

    def __init__(self, name, pm_2_5, pm_10, n2o):
        """Initialize the Demo Air Quality."""
        print("GRAT creating service")
        self.connection=GratAirQualityConnection()
        print("GRAT  service created")
        #print("starting gogol")
        #self.gogol.start()
        #print("started, continuing with init")
        self._name = name
        self._pm_2_5 = pm_2_5
        self._pm_10 = pm_10
        self._pm_100 = pm_100
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return '{} {}'.format('GRAT Demo Air Quality', self._name)

    @property
    def should_poll(self):
        """Polling will talk to dripline"""

    @property
    def particulate_matter_2_5(self):
        """Return the particulate matter 2.5 level."""
        return self._pm_2_5

    @property
    def particulate_matter_10(self):
        """Return the particulate matter 10 level."""
        return self._pm_10

    @property
    def attribution(self):
        """Return the attribution."""
        return 'As per Kats request'

    def update(self):
        """talk ta dripline here, maybe better to by async"""
        #target, request
        logger.info("GRAT calling update")
        msgop = getattr(constants, 'OP_GET')
        request = message.RequestMessage(msgop=msgop, payload={})
        logger.info("GRAT request made ")
        result=self.connection.send_request("particle_density",request)
        logger.info("GRAT send_request with info {} ".format(result))
        if ("pm_2_5" in result) and ("pm_10" in result) and ("pm_100" in result):
            self._pm_2_5=result["pm_2_5"]
            self._pm_10=result["pm_10"]
            self._pm_100=result["pm_100"]
        logger.warning("GRAT results to pm25 sensor malformed, ignoring")
        return True
