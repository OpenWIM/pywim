

class Temperature:
    """
    Temperature class to correct the temperature influence

    """
    amplification_factor = 1.012860
    curve_slope = -0.005277
    sensitivity_factor = 0.0098
    offset = 0.4199
    gain_factor = 0.4659
    reference_temperature = 23.4695127139  # 28

    @classmethod
    def influence_correction_burnos(cls, temperature: float):
        """
        Temperature Correction of Measurement Data

        Temperature correction of the measurement data is possible as long as
        the site is pre-calibrated, for example by the pre-weighed vehicle
        method.

        The pre-calibration procedure should yield the fixed value of the
        calibration coefficient C_0.

        The sensitivity of the measurement system will change with the change
        of asphalt temperature and the weighing accuracy will be decreasing.
        In order to compensate for these adverse  effects, it is required that
        a relevant model be applied relating asphalt properties to  temperature
        changes, which is shown in an experimental characteristic in Fig 1. The
        characteristic was obtained on a multi-sensor WIM site (first axle load
        of reference vehicles taken into account), equipped with piezoelectric
        sensors mounted in the road surface in Gardawice (Poland).

        The model, fitted to measurement data, is written as (3):

        C_T(T_a) = k_1 * 10^(w_1 * (T_0 - T_a)

        where:
        C_T - temperature coefficient
        T_a - asphalt temperature [C],
        k_1 = 1,012860 - amplification factor,
        w_1 = −0,005277 - curve slope,
        T_0 = 10 - reference temperature expressed in [C]

        The model (3) expresses the relationship between asphalt temperature
        and stiffness (thus weighting results). This relation is well-known
        from literature on the subject (Lukanen, 2000). The coefficient w_1 ,
        associated with the asphalt type and composition, may assume negative
        values, implying that stiffness of the road surface decreases with
        increasing temperatures and the load exerted upon the sensor will
        increase, too. Temperature compensation involves the computation of C_T
        value and modification of weighing results, in accordance with the (4).

        W_ST = (1 / (C_0*C_T)) * W_d

        where:
        C_0 - fixed calibration coefficient determined by the pre-weighed
            vehicle method,
        W_ST - calibrated weighing data taking into account temperature
            correction, i.e. gross weight or static load of an axle.
        W_d - not calibrated data obtained from processing of the load signals
            from WIM sensors.

        Ongoing measurements of asphalt temperature ensures the updating of all
        weighing data, which is a major advantage of the applied method.
        However this correction compensates only for the influence of weighing
        results on asphalt temperature whilst the accuracy of the method
        largely depends on the model (3) accuracy. Besides, the final accuracy
        is affected by the accuracy of the pre-calibration procedure.

        :param temperature:
        :return: temperature influence correction

        Reference:

        AUTO-CALIBRATION AND TEMPERATURE CORRECTION OF WIM SYSTEMS
        Piotr BURNOS
        University of Science and Technology - Krakow, Poland

        """

        return cls.amplification_factor * 10**(
            cls.curve_slope * (cls.reference_temperature - temperature)
        )

    @classmethod
    def influence_correction_gajda(cls, temperature: float):
        """
        THE INFLUENCE OF TEMPERATURE ON ERRORS OF WIM SYSTEMS
        EMPLOYING PIEZOELECTRIC SENSORS

        In order to compute the axle load value W the signal U 0 is processed
        according to algorithm (1) provided by the sensor manufacturer.

        The results shown in Figure 10 (points 1) can be described with good
        accuracy by the model in the form of (4) [11] (curve 2).

        C_T(T_a) = k_T × 10^(w_T × (T_a)) + b_T

        where:
            T_a – asphalt temperature [°C],
            k_T = 0.4659 – gain factor,
            w_T = 0.0098 – sensitivity factor,
            b_T = 0.4199 – offset.

        Coefficients k T , w T , b T depend on the asphalt components and
        should be determined separately for each site.
        The knowledge of the model (4) enables online correction of the
        weighing error but it requires continuous measuring of the road
        pavement temperature at a depth similar to that at which the load
        sensors are installed. As follows from Figure 10 the relative weighing
        error in a WIM system where such correction has not been implemented
        may attain even 30%.

        Reference:

        THE INFLUENCE OF TEMPERATURE ON ERRORS OF WIM SYSTEMS
        EMPLOYING PIEZOELECTRIC SENSORS

        Janusz Gajda 1) , Ryszard Sroka 1) , Tadeusz Zeglen 1) ,
        Piotr Burnos 1)
        1) AGH University of Science and Technology, Al. A. Mickiewicza 30,
        30-059 Krakow, Poland (*jgajda@agh.edu.pl)

        """
        return cls.gain_factor * (
            10**(cls.sensitivity_factor * temperature)
        ) + cls.offset
