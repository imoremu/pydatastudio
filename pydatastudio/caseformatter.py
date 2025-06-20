from string import Formatter

class CaseFormatter(Formatter):
    """An extended format string formatter

    Formatter with extended conversion symbol
    """
    def convert_field(self, value, conversion):
        """ Extend conversion symbol
        Following additional symbol has been added
        * l: convert to string and low case
        * u: convert to string and up case

        default are:
        * s: convert with str()
        * r: convert with repr()
        * a: convert with ascii()
        """

        if conversion == "u":
            return str(value).upper()
        elif conversion == "l":
            return str(value).lower()
        elif conversion == "c":
            return str(value)[0].upper() + str(value)[1:].lower()
        elif conversion == "f":
            return str(value)[0].lower() + str(value)[1:].upper()
            
                      
        # Do the default conversion or raise error if no matching conversion found
        super(CaseFormatter, self).convert_field(value, conversion)

        # return for None case
        return value