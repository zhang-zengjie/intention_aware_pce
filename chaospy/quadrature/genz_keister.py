"""
Hermite Genz-Keister quadrature rules

Adapted from John Burkardt's implementation in Matlab
"""
import numpy
import scipy

from .utils import combine_quadrature

GENZ_KEISTER_STORE = {
    1: ((0.0000000000000000e00,), (1.7724538509055159,)),
    3: (
        (0.0000000000000000e00, 1.2247448713915889),
        (1.1816359006036772, 0.29540897515091930),
    ),
    7: (
        (
            0.0000000000000000,
            0.52403354748695763,
            1.2247448713915889,
            2.9592107790638380,
        ),
        (
            0.81310410832613500,
            0.23286251787386100,
            0.24557928535031393,
            0.0012330680655153448,
        ),
    ),
    9: (
        (
            0.0000000000000000,
            0.52403354748695763,
            1.2247448713915889,
            2.0232301911005157,
            2.9592107790638380,
        ),
        (
            0.45014700975378197,
            0.47869428549114124,
            0.16811892894767771,
            0.014173117873979098,
            1.6708826306882348e-4,
        ),
    ),
    17: (
        (
            0.0000000000000000,
            0.52403354748695763,
            0.87004089535290285,
            1.2247448713915889,
            1.8357079751751868,
            2.0232301911005157,
            2.9592107790638380,
            3.6677742159463378,
            4.4995993983103881,
        ),
        (
            0.47310733504965385,
            0.45119803602358544,
            0.025155825701712934,
            0.15718298376652240,
            0.0034840719346803800,
            0.012466519132805918,
            1.8723818949278350e-04,
            -1.4542843387069391e-06,
            3.7463469943051758e-08,
        ),
    ),
    19: (
        (
            0.0000000000000000,
            0.52403354748695763,
            0.87004089535290285,
            1.2247448713915889,
            1.8357079751751868,
            2.0232301911005157,
            2.2665132620567876,
            2.9592107790638380,
            3.6677742159463378,
            4.4995993983103881,
        ),
        (
            0.53788160700510168,
            0.36924643368920851,
            0.10838861955003017,
            0.11360729895748269,
            0.032055243099445879,
            -0.011232438489069229,
            5.1133174390883855e-03,
            1.0656589772852267e-04,
            1.0802767206624762e-06,
            1.5295717705322357e-09,
        ),
    ),
    31: (
        (
            0.0000000000000000,
            0.17606414208200893,
            0.52403354748695763,
            0.87004089535290285,
            1.2247448713915889,
            1.5794121348467671,
            1.8357079751751868,
            2.0232301911005157,
            2.2665132620567876,
            2.5705583765842968,
            2.9592107790638380,
            3.6677742159463378,
            4.4995993983103881,
            5.0360899444730940,
            5.6432578578857449,
            6.3759392709822356,
        ),
        (
            0.45888839636756751,
            0.049855761893293160,
            0.35393889029580544,
            0.11594930984853116,
            0.10939325071860877,
            0.0031210210352682834,
            0.029409427580350787,
            -0.0098566270434610019,
            0.0048385208205502612,
            2.6665159778939428e-05,
            1.0541662394746661e-04,
            1.0889219692128120e-06,
            1.4055252024722478e-09,
            9.0675288231679823e-12,
            -2.6304696458548942e-13,
            2.2365645607044459e-15,
        ),
    ),
    33: (
        (
            0.0000000000000000,
            0.17606414208200893,
            0.52403354748695763,
            0.87004089535290285,
            1.2247448713915889,
            1.5794121348467671,
            1.8357079751751868,
            2.0232301911005157,
            2.2665132620567876,
            2.5705583765842968,
            2.9592107790638380,
            3.6677742159463378,
            4.0292201405043713,
            4.4995993983103881,
            5.0360899444730940,
            5.6432578578857449,
            6.3759392709822356,
        ),
        (
            2.4656644932829619e-01,
            1.8411696047725790e-01,
            3.1208656194697448e-01,
            1.3726521191567551e-01,
            9.6913444944583621e-02,
            1.3032872699027960e-02,
            2.0435058359107205e-02,
            -4.9118576123877555e-03,
            3.7580026604304793e-03,
            1.4753204901862772e-04,
            9.8710009197409173e-05,
            1.2245220967158438e-06,
            -2.3903343382803510e-08,
            2.7547825138935901e-09,
            -3.4281570530349562e-11,
            4.7219278666417693e-13,
            -1.7602932805372496e-15,
        ),
    ),
    35: (
        (
            0.0000000000000000e00,
            1.7606414208200893e-01,
            5.2403354748695763e-01,
            8.7004089535290285e-01,
            1.2247448713915889e00,
            1.5794121348467671e00,
            1.8357079751751868e00,
            2.0232301911005157e00,
            2.2665132620567876e00,
            2.5705583765842968e00,
            2.9592107790638380e00,
            3.3491639537131945e00,
            3.6677742159463378e00,
            4.0292201405043713e00,
            4.4995993983103881e00,
            5.0360899444730940e00,
            5.6432578578857449e00,
            6.3759392709822356e00,
        ),
        (
            9.1262675363737921e-04,
            3.3988595585585218e-01,
            2.6244871488784277e-01,
            1.6371221555735804e-01,
            8.0245518147390893e-02,
            2.7780508908535097e-02,
            5.5928828911469180e-03,
            4.0967527720344047e-03,
            1.4515580425155904e-03,
            4.8785399304443770e-04,
            6.3328620805617891e-05,
            4.8462799737020461e-06,
            4.3737818040926989e-07,
            3.7920222392319532e-08,
            8.1553721816916897e-10,
            5.4896836948499462e-12,
            9.6599466278563243e-15,
            1.8684014894510604e-18,
        ),
    ),
    37: (
        (
            0.000000000000000,
            0.214618180588171,
            0.524033547486958,
            0.870040895352903,
            1.224744871391589,
            1.561553427651873,
            1.835707975175187,
            2.023230191100516,
            2.266513262056788,
            2.597288631188366,
            2.959210779063838,
            3.315584617593290,
            3.667774215946338,
            4.057956316089741,
            4.499599398310388,
            4.986551454150765,
            5.521865209868350,
            6.124527854622158,
            6.853200069757519,
        ),
        (
            0.968824552928425499e-01,
            0.147655710402686249e00,
            0.143099302896833389e00,
            0.937208280655245902e-01,
            0.442116442189845444e-01,
            0.15513109874859354e-01,
            0.43334988122723492e-02,
            0.176802225818295443e-02,
            0.985827582996483824e-03,
            0.234940366465975222e-03,
            0.32265185983739747e-04,
            0.330975870979203419e-05,
            0.295907520230744049e-06,
            0.16595448809389819e-07,
            0.422525843963111041e-09,
            0.45661763676186859e-11,
            0.182242751549129356e-13,
            0.187781893143728947e-16,
            0.19030350940130498e-20,
        ),
    ),
    41: (
        (
            0.0000000000000000,
            0.195324784415805,
            0.52403354748695763,
            0.87004089535290285,
            1.2247448713915889,
            1.585873011819188,
            1.8357079751751868,
            2.0232301911005157,
            2.043834754429505,
            2.2665132620567876,
            2.630415236459871,
            2.9592107790638380,
            3.296114596212218,
            3.6677742159463378,
            4.070919267883068,
            4.4995993983103881,
            4.953574342912980,
            5.437443360177798,
            5.961461043404500,
            6.547083258397540,
            7.251792998192644,
        ),
        (
            0.562793426043218877e-01,
            0.165639740400529554e00,
            0.145966293895926429e00,
            0.928338228510111845e-01,
            0.45109010335859128e-01,
            0.165445526705860772e-01,
            0.705471110122962612e-03,
            0.178852543033699732e-01,
            -0.144528422206988237e-01,
            0.140697424065246825e-02,
            0.189010909805097887e-03,
            0.288976780274478689e-04,
            0.381182791749177506e-05,
            0.315372265852264871e-06,
            0.149158210417831408e-07,
            0.400784141604834759e-09,
            0.581803393170320419e-11,
            0.408820161202505983e-13,
            0.1140700785308509e-15,
            0.860427172512207236e-19,
            0.664195893812757801e-23,
        ),
    ),
    43: (
        (
            0.0000000000000000,
            0.196029453662011,
            0.52403354748695763,
            0.87004089535290285,
            1.2247448713915889,
            1.583643465293944,
            1.8357079751751868,
            2.0232301911005157,
            2.089340389294661,
            2.2665132620567876,
            2.633356763661946,
            2.9592107790638380,
            3.295265921534226,
            3.6677742159463378,
            4.071335874253583,
            4.4995993983103881,
            4.952329763008589,
            5.434053000365068,
            5.954781975039809,
            6.535398426382995,
            7.231746029072501,
            10.167574994881873,
        ),
        (
            0.579595986101181095e-01,
            0.164880913687436689e00,
            0.145863292632147353e00,
            0.928711584442575456e-01,
            0.450612329041864976e-01,
            0.163616873493832402e-01,
            0.139966252291568061e-02,
            0.67354758901013295e-02,
            -0.38799558623877157e-02,
            0.150909333211638847e-02,
            0.184789465688357423e-03,
            0.286802318064777813e-04,
            0.383880761947398577e-05,
            0.316018363221289247e-06,
            0.148653643571796457e-07,
            0.400030575425776948e-09,
            0.586915885251734856e-11,
            0.421921851448196032e-13,
            0.122619614947864357e-15,
            0.992619971560149097e-19,
            0.87544909871323873e-23,
            0.546191947478318097e-37,
        ),
    ),
}

RULES = {
    16: [1, 3, 7, 9, 17, 19, 31],
    18: [1, 3, 9, 19, 37],
    22: [1, 3, 9, 19, 41],
    24: [1, 3, 9, 19, 43],
}


def genz_keister_16(order, dist=None):
    """
    Create Genz-Keister variant 16 quadrature nodes and weights.

    Args:
        order (int, Sequence[int]):
            The order of the quadrature.
        dist (Optional[chaospy.Distribution]):
            The distribution which density will be used as weight function.
            If omitted, standard Gaussian is assumed.

    Returns:
        (numpy.ndarray, numpy.ndarray):
            Genz-Keister quadrature abscissas and weights.

    Examples:
        >>> nodes, weights = genz_keister_16(4)
        >>> nodes.round(2)
        array([[-6.36, -5.19, -4.18, -2.86, -2.6 , -1.73, -1.23, -0.74,  0.  ,
                 0.74,  1.23,  1.73,  2.6 ,  2.86,  4.18,  5.19,  6.36]])
        >>> weights.round(8)
        array([ 2.0000000e-08, -8.2000000e-07,  1.0564000e-04,  7.0334800e-03,
                1.9656800e-03,  8.8681000e-02,  1.4192650e-02,  2.5456123e-01,
                2.6692223e-01,  2.5456123e-01,  1.4192650e-02,  8.8681000e-02,
                1.9656800e-03,  7.0334800e-03,  1.0564000e-04, -8.2000000e-07,
                2.0000000e-08])

    """
    return genz_keister(order, dist, rule=16)


def genz_keister_18(order, dist=None):
    """
    Create Genz-Keister variant 18 quadrature nodes and weights.

    Args:
        order (int, Sequence[int]):
            The order of the quadrature.
        dist (Optional[chaospy.Distribution]):
            The distribution which density will be used as weight function.
            If omitted, standard Gaussian is assumed.

    Returns:
        (numpy.ndarray, numpy.ndarray):
            Genz-Keister quadrature abscissas and weights.

    Examples:
        >>> nodes, weights = genz_keister_18(2)
        >>> nodes.round(2)
        array([[-4.18, -2.86, -1.73, -0.74,  0.  ,  0.74,  1.73,  2.86,  4.18]])
        >>> weights.round(8)
        array([9.4270000e-05, 7.9963300e-03, 9.4850950e-02, 2.7007433e-01,
               2.5396825e-01, 2.7007433e-01, 9.4850950e-02, 7.9963300e-03,
               9.4270000e-05])

    """
    return genz_keister(order, dist, rule=18)


def genz_keister_22(order, dist=None):
    """
    Create Genz-Keister variant 22 quadrature nodes and weights.

    Args:
        order (int, Sequence[int]):
            The order of the quadrature.
        dist (Optional[chaospy.Distribution]):
            The distribution which density will be used as weight function.
            If omitted, standard Gaussian is assumed.

    Returns:
        (numpy.ndarray, numpy.ndarray):
            Genz-Keister quadrature abscissas and weights.

    Examples:
        >>> nodes, weights = genz_keister_22(2)
        >>> nodes.round(2)
        array([[-4.18, -2.86, -1.73, -0.74,  0.  ,  0.74,  1.73,  2.86,  4.18]])
        >>> weights.round(8)
        array([9.4270000e-05, 7.9963300e-03, 9.4850950e-02, 2.7007433e-01,
               2.5396825e-01, 2.7007433e-01, 9.4850950e-02, 7.9963300e-03,
               9.4270000e-05])

    """
    return genz_keister(order, dist, rule=22)


def genz_keister_24(order, dist=None):
    """
    Create Genz-Keister variant 24 quadrature nodes and weights.

    Args:
        order (int, Sequence[int]):
            The order of the quadrature.
        dist (Optional[chaospy.Distribution]):
            The distribution which density will be used as weight function.
            If omitted, standard Gaussian is assumed.

    Returns:
        (numpy.ndarray, numpy.ndarray):
            Genz-Keister quadrature abscissas and weights.

    Examples:
        >>> nodes, weights = genz_keister_24(2)
        >>> nodes.round(2)
        array([[-4.18, -2.86, -1.73, -0.74,  0.  ,  0.74,  1.73,  2.86,  4.18]])
        >>> weights.round(8)
        array([9.4270000e-05, 7.9963300e-03, 9.4850950e-02, 2.7007433e-01,
               2.5396825e-01, 2.7007433e-01, 9.4850950e-02, 7.9963300e-03,
               9.4270000e-05])

    """
    return genz_keister(order, dist, rule=24)


def genz_keister(order, dist=None, rule=24):
    """
    Create Genz-Keister quadrature nodes and weights.

    Args:
        order (int, Sequence[int]):
            The order of the quadrature.
        dist (Optional[chaospy.Distribution]):
            The distribution which density will be used as weight function.
            If omitted, standard Gaussian is assumed.
        rule (int, Sequence[int]):
            The Genz-Keister rule name. Supported rules are 16, 18, 22 and 24.

    Returns:
        (numpy.ndarray, numpy.ndarray):
            Genz-Keister quadrature abscissas and weights.

    Examples:
        >>> genz_keister(0)
        (array([[0.]]), array([1.]))
        >>> genz_keister(1)  # doctest: +NORMALIZE_WHITESPACE
        (array([[-1.73205081,  0.        ,  1.73205081]]),
         array([0.16666667, 0.66666667, 0.16666667]))

    """
    shape = (1,) if dist is None else (len(dist),)
    order = numpy.broadcast_to(order, shape)
    rule = numpy.broadcast_to(rule, shape)
    nodes, weights = zip(
        *[_genz_keister(order_, rule_) for order_, rule_ in zip(order, rule)]
    )
    nodes, weights = combine_quadrature(nodes, weights)
    if dist is not None:
        nodes = dist.inv(scipy.special.ndtr(nodes))
    return nodes, weights


def _genz_keister(order, rule):
    assert rule in RULES, "rule %d not in known rules: %s" % (rule, list(RULES))
    assert order <= len(RULES[rule]), "rule genz_keister_%d limited at order %d" % (
        rule,
        order,
    )
    order = RULES[rule][order]
    nodes, weights = GENZ_KEISTER_STORE[order]
    length = len(nodes)
    nodes = numpy.array(nodes[::-1] + nodes[1:])
    nodes[: length - 1] *= -1
    nodes *= numpy.sqrt(2)
    weights = numpy.array(weights[::-1] + weights[1:])
    weights /= numpy.sum(weights)

    return nodes, weights
