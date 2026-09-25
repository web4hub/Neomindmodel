<cfcomponent
    displayname="NeomindBoard"
    output="false">

    <cffunction
        name="getSpecification"
        access="public"
        returntype="struct"
        output="false">

        <cfreturn {
            board = "Neomind Board v1",
            mcu = "ATmega328P",
            clock = "16MHz",
            flash = "32KB",
            sram = "2KB",
            digitalPins = 14,
            analogPins = 6,
            pwmPins = [3,5,6,9,10,11]
        }>
    </cffunction>

</cfcomponent>
