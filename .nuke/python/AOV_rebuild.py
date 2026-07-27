import nuke
import nukescripts
import re
import collections

## global Variables
LIGHTGROUP_REGEX = re.compile(r'^(?!.*filter)(?=.*(?:light|lghts?|lgh|lg|lts?|hdri?))[a-z0-9]+(?:__?[a-z0-9]+)*$', re.IGNORECASE)

ARNOLD_ADDITIONAL_LIGHTING = {
    'direct': re.compile(r'^_{0,2}direct_{0,2}$', re.IGNORECASE),
    'indirect': re.compile(r'^_{0,2}indirect_{0,2}$', re.IGNORECASE),
}

KARMA_ADDITIONAL_LIGHTING = {}

# REDSHIFT_ADDITIONAL_LIGHTING = {}

RENDERMAN_ADDITIONAL_LIGHTING = {}

VRAY_ADDITIONAL_LIGHTING = {
    'Total_Light': re.compile(r'^_{0,2}total_{0,2}light_{0,2}$', re.IGNORECASE),
    'Light_Select': re.compile(r'^_{0,2}light_{0,2}select_{0,2}$', re.IGNORECASE),
    'Raw_Total_Light': re.compile(r'^_{0,2}raw_{0,2}total_{0,2}light_{0,2}$', re.IGNORECASE),
}

GENERIC_ADDITIONAL_LIGHTING = {
    'direct': re.compile(r'^_{0,2}direct_{0,2}$', re.IGNORECASE),
    'indirect': re.compile(r'^_{0,2}indirect_{0,2}$', re.IGNORECASE),
    'Total_Light': re.compile(r'^_{0,2}total_{0,2}light_{0,2}$', re.IGNORECASE),
    'Raw_Total_Light': re.compile(r'^_{0,2}raw_{0,2}total_{0,2}light_{0,2}$', re.IGNORECASE),
    'Light_Select': re.compile(r'^_{0,2}light_{0,2}select_{0,2}$', re.IGNORECASE),
}

ARNOLD_MATERIALS = {
    'albedo': re.compile(r'^_{0,2}albedo_{0,2}$', re.IGNORECASE),
    'diffuse_albedo': re.compile(r'^_{0,2}(?:diffuse_{0,2}albedo|albedo_{0,2}diffuse)_{0,2}$', re.IGNORECASE),
    'diffuse': re.compile(r'^_{0,2}diffuse_{0,2}$', re.IGNORECASE),
    'diffuse_direct': re.compile(r'^_{0,2}(?:diffuse_{0,2}direct|direct_{0,2}diffuse)_{0,2}$', re.IGNORECASE),
    'diffuse_indirect': re.compile(r'^_{0,2}(?:diffuse_{0,2}indirect|indirect_{0,2}diffuse)_{0,2}$', re.IGNORECASE),
    'sss': re.compile(r'^_{0,2}sss_{0,2}$', re.IGNORECASE),
    'sss_albedo': re.compile(r'^_{0,2}(?:sss_{0,2}albedo|albedo_{0,2}sss)_{0,2}$', re.IGNORECASE),
    'sss_direct': re.compile(r'^_{0,2}(?:sss_{0,2}direct|direct_{0,2}sss)_{0,2}$', re.IGNORECASE),
    'sss_indirect': re.compile(r'^_{0,2}(?:sss_{0,2}indirect|indirect_{0,2}sss)_{0,2}$', re.IGNORECASE),
    'coat': re.compile(r'^_{0,2}coat_{0,2}$', re.IGNORECASE),
    'coat_albedo': re.compile(r'^_{0,2}(?:coat_{0,2}albedo|albedo_{0,2}coat)_{0,2}$', re.IGNORECASE),
    'coat_direct': re.compile(r'^_{0,2}(?:coat_{0,2}direct|direct_{0,2}coat)_{0,2}$', re.IGNORECASE),
    'coat_indirect': re.compile(r'^_{0,2}(?:coat_{0,2}indirect|indirect_{0,2}coat)_{0,2}$', re.IGNORECASE),
    'sheen': re.compile(r'^_{0,2}sheen_{0,2}$', re.IGNORECASE),
    'sheen_albedo': re.compile(r'^_{0,2}(?:sheen_{0,2}albedo|albedo_{0,2}sheen)_{0,2}$', re.IGNORECASE),
    'sheen_direct': re.compile(r'^_{0,2}(?:sheen_{0,2}direct|direct_{0,2}sheen)_{0,2}$', re.IGNORECASE),
    'sheen_indirect': re.compile(r'^_{0,2}(?:sheen_{0,2}indirect|indirect_{0,2}sheen)_{0,2}$', re.IGNORECASE),
    'transmission': re.compile(r'^_{0,2}transmission_{0,2}$', re.IGNORECASE),
    'transmission_albedo': re.compile(r'^_{0,2}(?:transmission_{0,2}albedo|albedo_{0,2}transmission)_{0,2}$', re.IGNORECASE),
    'transmission_direct': re.compile(r'^_{0,2}(?:transmission_{0,2}direct|direct_{0,2}transmission)_{0,2}$', re.IGNORECASE),
    'transmission_indirect': re.compile(r'^_{0,2}(?:transmission_{0,2}indirect|indirect_{0,2}transmission)_{0,2}$', re.IGNORECASE),
    'caustics': re.compile(r'^_{0,2}caustics_{0,2}$', re.IGNORECASE),
    'refract': re.compile(r'^_{0,2}refract(?:ion)?_{0,2}$', re.IGNORECASE),
    'emission': re.compile(r'^_{0,2}emission_{0,2}$', re.IGNORECASE),
    'emission_direct': re.compile(r'^_{0,2}(?:emission_{0,2}direct|direct_{0,2}emission)_{0,2}$', re.IGNORECASE),
    'emission_indirect': re.compile(r'^_{0,2}(?:emission_{0,2}indirect|indirect_{0,2}emission)_{0,2}$', re.IGNORECASE),
    'volume': re.compile(r'^_{0,2}volume_{0,2}$', re.IGNORECASE),
    'volume_albedo': re.compile(r'^_{0,2}(?:volume_{0,2}albedo|albedo_{0,2}volume)_{0,2}$', re.IGNORECASE),
    'volume_direct': re.compile(r'^_{0,2}(?:volume_{0,2}direct|direct_{0,2}volume)_{0,2}$', re.IGNORECASE),
    'volume_indirect': re.compile(r'^_{0,2}(?:volume_{0,2}indirect|indirect_{0,2}volume)_{0,2}$', re.IGNORECASE),
    #'shadow': re.compile(r'^_{0,2}shadow_{0,2}$', re.IGNORECASE),
    #'shadow_diff': re.compile(r'^_{0,2}shadow_{0,2}diff(?:use)?_{0,2}$', re.IGNORECASE),
}

ARNOLD_UTILITIES = {
    'alpha': re.compile(r'^_{0,2}(?:alpha|A)_{0,2}$', re.IGNORECASE),
    'rgba': re.compile(r'^_{0,2}rgba_{0,2}$', re.IGNORECASE),
    'Z': re.compile(r'^_{0,2}(?:z_{0,2}depth|_{0,2}depth_{0,2}z|depth|Z)_{0,2}$', re.IGNORECASE),
    'P': re.compile(r'^_{0,2}(?:p|pos(?:ition)?)_{0,2}$', re.IGNORECASE),
    'P_camera': re.compile(r'^_{0,2}(?:p|pos(?:ition)?)_{0,2}cam(?:era)?_{0,2}$', re.IGNORECASE),
    'Pref': re.compile(r'^_{0,2}p_{0,2}ref(?:erence)?_{0,2}$', re.IGNORECASE),
    'N': re.compile(r'^_{0,2}(?:n(?:orm(?:als?)?)?)_{0,2}$', re.IGNORECASE),
    'motionvector': re.compile(r'^_{0,2}motion_{0,2}vectors?_{0,2}$', re.IGNORECASE),
    'opacity': re.compile(r'^_{0,2}opacity_{0,2}$', re.IGNORECASE),
    'volume_opacity': re.compile(r'^_{0,2}volume_{0,2}opacity_{0,2}$', re.IGNORECASE),
    #'ID': re.compile(r'^_{0,2}(?:ID?_{0,2}[0-9]+)_{0,2}$', re.IGNORECASE),
    'AA_inv_density': re.compile(r'^_{0,2}aa_{0,2}inv_{0,2}density_{0,2}$', re.IGNORECASE),
    'cputime': re.compile(r'^_{0,2}cpu_{0,2}time_{0,2}$', re.IGNORECASE),
}

KARMA_MATERIALS = {
    'albedo': re.compile(r'^_{0,2}albedo_{0,2}$', re.IGNORECASE),
    'albedodiffuse': re.compile(r'^_{0,2}(?:albedo_{0,2}diffuse|diffuse_{0,2}albedo)_{0,2}$', re.IGNORECASE),
    'combineddiffuse': re.compile(r'^_{0,2}combined_{0,2}diffuse_{0,2}$', re.IGNORECASE),
    'directdiffuse': re.compile(r'^_{0,2}direct_{0,2}diffuse_{0,2}$', re.IGNORECASE),
    'indirectdiffuse': re.compile(r'^_{0,2}indirect_{0,2}diffuse_{0,2}$', re.IGNORECASE),
    'sss': re.compile(r'^_{0,2}sss_{0,2}$', re.IGNORECASE),
    'combinedglossyreflection': re.compile(r'^_{0,2}combined_{0,2}glossy_{0,2}reflection_{0,2}$', re.IGNORECASE),
    'directglossyreflection': re.compile(r'^_{0,2}direct_{0,2}glossy_{0,2}reflection_{0,2}$', re.IGNORECASE),
    'indirectglossyreflection': re.compile(r'^_{0,2}indirect_{0,2}glossy_{0,2}reflection_{0,2}$', re.IGNORECASE),
    'coat': re.compile(r'^_{0,2}coat_{0,2}$', re.IGNORECASE),
    'glossytransmission': re.compile(r'^_{0,2}glossy_{0,2}transmission_{0,2}$', re.IGNORECASE),
    'refract': re.compile(r'^_{0,2}refract(?:ion)?_{0,2}$', re.IGNORECASE),
    'caustics': re.compile(r'^_{0,2}caustics_{0,2}$', re.IGNORECASE),
    'combinedemission': re.compile(r'^_{0,2}combined_{0,2}emission_{0,2}$', re.IGNORECASE),
    'directemission': re.compile(r'^_{0,2}direct_{0,2}emission_{0,2}$', re.IGNORECASE),
    'indirectemission': re.compile(r'^_{0,2}indirect_{0,2}emission_{0,2}$', re.IGNORECASE),
    'combinedvolume': re.compile(r'^_{0,2}combined_{0,2}volume_{0,2}$', re.IGNORECASE),
    'directvolume': re.compile(r'^_{0,2}direct_{0,2}volume_{0,2}$', re.IGNORECASE),
    'indirectvolume': re.compile(r'^_{0,2}indirect_{0,2}volume_{0,2}$', re.IGNORECASE),
    #'shadow': re.compile(r'^_{0,2}shadow_{0,2}$', re.IGNORECASE),
    #'combineddiffuseshadow': re.compile(r'^_{0,2}combined_{0,2}diffuse_{0,2}shadow_{0,2}$', re.IGNORECASE),
    #'directdiffuseshadow': re.compile(r'^_{0,2}direct_{0,2}diffuse_{0,2}shadow_{0,2}$', re.IGNORECASE),
    #'indirectdiffuseshadow': re.compile(r'^_{0,2}indirect_{0,2}diffuse_{0,2}shadow_{0,2}$', re.IGNORECASE),
    #'beautyunshadowed': re.compile(r'^_{0,2}beauty_{0,2}unshadowed_{0,2}$', re.IGNORECASE),
    #'combineddiffuseunshadowed': re.compile(r'^_{0,2}combined_{0,2}diffuse_{0,2}unshadowed_{0,2}$', re.IGNORECASE),
    #'directdiffuseunshadowed': re.compile(r'^_{0,2}direct_{0,2}diffuse_{0,2}unshadowed_{0,2}$', re.IGNORECASE),
    #'indirectdiffuseunshadowed': re.compile(r'^_{0,2}indirect_{0,2}diffuse_{0,2}unshadowed_{0,2}$', re.IGNORECASE),
    #'ao': re.compile(r'^_{0,2}ao_{0,2}$', re.IGNORECASE),
}

KARMA_UTILITIES = {
    'alpha': re.compile(r'^_{0,2}(?:alpha|A)_{0,2}$', re.IGNORECASE),
    'rgba': re.compile(r'^_{0,2}rgba_{0,2}$', re.IGNORECASE),
    'depth_extra': re.compile(r'^_{0,2}depth_{0,2}extra_{0,2}$', re.IGNORECASE),
    'P': re.compile(r'^_{0,2}(?:p|pos(?:ition)?)_{0,2}$', re.IGNORECASE),
    'P_camera': re.compile(r'^_{0,2}(?:p|pos(?:ition)?)_{0,2}cam(?:era)?_{0,2}$', re.IGNORECASE),
    'pRef': re.compile(r'^_{0,2}p_{0,2}ref(?:erence)?_{0,2}$', re.IGNORECASE),
    'N': re.compile(r'^_{0,2}(?:n|normals?)_{0,2}$', re.IGNORECASE),
    'Ng': re.compile(r'^_{0,2}ng_{0,2}$', re.IGNORECASE),
    'motionvectors': re.compile(r'^_{0,2}motion_{0,2}vectors?_{0,2}$', re.IGNORECASE),
    'velocity': re.compile(r'^_{0,2}velocity_{0,2}$', re.IGNORECASE),
    'uv_extra': re.compile(r'^_{0,2}uv_{0,2}extra_{0,2}$', re.IGNORECASE),
    'Facingratio_N': re.compile(r'^_{0,2}facing_{0,2}ratio_{0,2}n_{0,2}$', re.IGNORECASE),
    'Facingratio_Ng': re.compile(r'^_{0,2}facing_{0,2}ratio_{0,2}ng_{0,2}$', re.IGNORECASE),
    'indirectraycount': re.compile(r'^_{0,2}indirect_{0,2}ray_{0,2}count_{0,2}$', re.IGNORECASE),
    'primarysamples': re.compile(r'^_{0,2}primary_{0,2}samples_{0,2}$', re.IGNORECASE),
    'cputime': re.compile(r'^_{0,2}cpu_{0,2}time_{0,2}$', re.IGNORECASE),
    'oraclevariance': re.compile(r'^_{0,2}oracle_{0,2}variance_{0,2}$', re.IGNORECASE),
}

RENDERMAN_MATERIALS = {
    'beauty': re.compile(r'^_{0,2}(?:beauty|c?olor)_{0,2}$', re.IGNORECASE),
    'albedo': re.compile(r'^_{0,2}albedo_{0,2}$', re.IGNORECASE),
    'diffuse': re.compile(r'^_{0,2}diffuse_{0,2}$', re.IGNORECASE),
    'directDiffuse': re.compile(r'^_{0,2}direct_{0,2}diffuse_{0,2}$', re.IGNORECASE),
    'directDiffuseLobe': re.compile(r'^_{0,2}direct_{0,2}diffuse_{0,2}lobe_{0,2}$', re.IGNORECASE),
    'directDiffuseUnoccluded': re.compile(r'^_{0,2}direct_{0,2}diffuse_{0,2}unoccluded_{0,2}$', re.IGNORECASE),
    'indirectDiffuseUnoccluded': re.compile(r'^_{0,2}indirect_{0,2}diffuse_{0,2}unoccluded_{0,2}$', re.IGNORECASE),
    'indirectDiffuse': re.compile(r'^_{0,2}indirect_{0,2}diffuse_{0,2}$', re.IGNORECASE),
    'indirectDiffuseLobe': re.compile(r'^_{0,2}indirect_{0,2}diffuse_{0,2}lobe_{0,2}$', re.IGNORECASE),
    'sss': re.compile(r'^_{0,2}sss_{0,2}$', re.IGNORECASE),
    'subsurface': re.compile(r'^_{0,2}subsurface_{0,2}$', re.IGNORECASE),
    'subsurfaceLobe': re.compile(r'^_{0,2}subsurface_{0,2}lobe_{0,2}$', re.IGNORECASE),
    'specular': re.compile(r'^_{0,2}specular_{0,2}$', re.IGNORECASE),
    'directSpecular': re.compile(r'^_{0,2}direct_{0,2}specular_{0,2}$', re.IGNORECASE),
    #'directSpecularPrimaryLobe': re.compile(r'^_{0,2}direct_{0,2}specular_{0,2}primary_{0,2}lobe_{0,2}$', re.IGNORECASE),
    'directSpecularUnoccluded': re.compile(r'^_{0,2}direct_{0,2}specular_{0,2}unoccluded_{0,2}$', re.IGNORECASE),
    'indirectSpecular': re.compile(r'^_{0,2}indirect_{0,2}specular_{0,2}$', re.IGNORECASE),
    #'indirectSpecularPrimaryLobe': re.compile(r'^_{0,2}indirect_{0,2}specular_{0,2}primary_{0,2}lobe_{0,2}$', re.IGNORECASE),
    #'directSpecularClearcoatLobe': re.compile(r'^_{0,2}direct_{0,2}specular_{0,2}clearcoat_{0,2}lobe_{0,2}$', re.IGNORECASE),
    #'directSpecularFuzzLobe': re.compile(r'^_{0,2}direct_{0,2}specular_{0,2}fuzz_{0,2}lobe_{0,2}$', re.IGNORECASE),
    #'directSpecularGlassLobe': re.compile(r'^_{0,2}direct_{0,2}specular_{0,2}glass_{0,2}lobe_{0,2}$', re.IGNORECASE),
    #'directSpecularIridescenceLobe': re.compile(r'^_{0,2}direct_{0,2}specular_{0,2}iridescence_{0,2}lobe_{0,2}$', re.IGNORECASE),
    #'directSpecularRoughLobe': re.compile(r'^_{0,2}direct_{0,2}specular_{0,2}rough_{0,2}lobe_{0,2}$', re.IGNORECASE),
    #'indirectSpecularClearcoatLobe': re.compile(r'^_{0,2}indirect_{0,2}specular_{0,2}clearcoat_{0,2}lobe_{0,2}$', re.IGNORECASE),
    #'indirectSpecularFuzzLobe': re.compile(r'^_{0,2}indirect_{0,2}specular_{0,2}fuzz_{0,2}lobe_{0,2}$', re.IGNORECASE),
    #'indirectSpecularGlassLobe': re.compile(r'^_{0,2}indirect_{0,2}specular_{0,2}glass_{0,2}lobe_{0,2}$', re.IGNORECASE),
    #'indirectSpecularIridescenceLobe': re.compile(r'^_{0,2}indirect_{0,2}specular_{0,2}iridescence_{0,2}lobe_{0,2}$', re.IGNORECASE),
    #'indirectSpecularRoughLobe': re.compile(r'^_{0,2}indirect_{0,2}specular_{0,2}rough_{0,2}lobe_{0,2}$', re.IGNORECASE),
    ##'indirectSpecularUnoccluded': re.compile(r'^_{0,2}indirect_{0,2}specular_{0,2}unoccluded_{0,2}$', re.IGNORECASE),
    'coat': re.compile(r'^_{0,2}coat_{0,2}$', re.IGNORECASE),
    #'transmission': re.compile(r'^_{0,2}transmission_{0,2}$', re.IGNORECASE),
    'transmissiveGlassLobe': re.compile(r'^_{0,2}transmissive_{0,2}glass_{0,2}lobe_{0,2}$', re.IGNORECASE),
    'transmissiveSingleScatterLobe': re.compile(r'^_{0,2}transmissive_{0,2}single_{0,2}scatter_{0,2}lobe_{0,2}$', re.IGNORECASE),
    'refract': re.compile(r'^_{0,2}refract(?:ion)?_{0,2}$', re.IGNORECASE),
    'caustics': re.compile(r'^_{0,2}caustics_{0,2}$', re.IGNORECASE),
    'emissive': re.compile(r'^_{0,2}emissive_{0,2}$', re.IGNORECASE),
    'directEmissive': re.compile(r'^_{0,2}direct_{0,2}emissive_{0,2}$', re.IGNORECASE),
    'indirectEmissive': re.compile(r'^_{0,2}indirect_{0,2}emissive_{0,2}$', re.IGNORECASE),
    'occluded': re.compile(r'^_{0,2}occluded_{0,2}$', re.IGNORECASE),
    'unoccluded': re.compile(r'^_{0,2}unoccluded_{0,2}$', re.IGNORECASE),
    #'shadow': re.compile(r'^_{0,2}shadow_{0,2}$', re.IGNORECASE),
}

RENDERMAN_UTILITIES = {
    'alpha': re.compile(r'^_{0,2}(?:alpha|a)_{0,2}$', re.IGNORECASE), # Absorbs 'a'
    'rgba': re.compile(r'^_{0,2}rgba_{0,2}$', re.IGNORECASE),
    'depth': re.compile(r'^_{0,2}(?:z_{0,2}depth|_{0,2}depth_{0,2}z|depth|Z)_{0,2}$', re.IGNORECASE), # Absorbs '__depth', 'z'
    'P': re.compile(r'^_{0,2}(?:p|pos(?:ition)?)_{0,2}$', re.IGNORECASE), # Absorbs 'Position'
    'P_camera': re.compile(r'^_{0,2}(?:p|pos(?:ition)?)_{0,2}cam(?:era)?_{0,2}$', re.IGNORECASE),
    'pRef': re.compile(r'^_{0,2}p_{0,2}ref(?:erence)?_{0,2}$', re.IGNORECASE), # Absorbs '__Pref'
    'normal': re.compile(r'^_{0,2}(?:normal|n)_{0,2}$', re.IGNORECASE),
    'nn': re.compile(r'^_{0,2}nn_{0,2}$', re.IGNORECASE), # Absorbs 'Nn'
    'motionvectors': re.compile(r'^_{0,2}motion_{0,2}vectors?_{0,2}$', re.IGNORECASE),
    'velocity': re.compile(r'^_{0,2}velocity_{0,2}$', re.IGNORECASE),
    'st': re.compile(r'^_{0,2}st_{0,2}$', re.IGNORECASE), # Absorbs '__st'
    'indirectraycount': re.compile(r'^_{0,2}indirect_{0,2}ray_{0,2}count_{0,2}$', re.IGNORECASE),
    'primId': re.compile(r'^_{0,2}prim_{0,2}id_{0,2}$', re.IGNORECASE),
    'instanceId': re.compile(r'^_{0,2}instance_{0,2}id_{0,2}$', re.IGNORECASE),
    'Ngn': re.compile(r'^_{0,2}ngn_{0,2}$', re.IGNORECASE),
    'Non': re.compile(r'^_{0,2}non_{0,2}$', re.IGNORECASE),
    'Oi': re.compile(r'^_{0,2}oi_{0,2}$', re.IGNORECASE),
    'PRadius': re.compile(r'^_{0,2}p_{0,2}radius_{0,2}$', re.IGNORECASE),
    'Po': re.compile(r'^_{0,2}po_{0,2}$', re.IGNORECASE),
    'Tn': re.compile(r'^_{0,2}tn_{0,2}$', re.IGNORECASE),
    'VLen': re.compile(r'^_{0,2}v_{0,2}len_{0,2}$', re.IGNORECASE),
    'Vn': re.compile(r'^_{0,2}vn_{0,2}$', re.IGNORECASE),
    'Nref': re.compile(r'^_{0,2}n_{0,2}ref_{0,2}$', re.IGNORECASE), # Absorbs '__Nref'
    'Nworld': re.compile(r'^_{0,2}n_{0,2}world_{0,2}$', re.IGNORECASE), # Absorbs '__Nworld'
    'Pworld': re.compile(r'^_{0,2}p_{0,2}world_{0,2}$', re.IGNORECASE), # Absorbs '__Pworld'
    'WNref': re.compile(r'^_{0,2}wn_{0,2}ref_{0,2}$', re.IGNORECASE), # Absorbs '__WNref'
    'WPref': re.compile(r'^_{0,2}wp_{0,2}ref_{0,2}$', re.IGNORECASE), # Absorbs '__WPref'
    'biasR': re.compile(r'^_{0,2}bias_{0,2}r_{0,2}$', re.IGNORECASE),
    'biasT': re.compile(r'^_{0,2}bias_{0,2}t_{0,2}$', re.IGNORECASE),
    'cpuTime': re.compile(r'^_{0,2}cpu_{0,2}time_{0,2}$', re.IGNORECASE),
    'curvature': re.compile(r'^_{0,2}curvature_{0,2}$', re.IGNORECASE),
    'dPcameradtime': re.compile(r'^_{0,2}d_{0,2}p_{0,2}camera_{0,2}d_{0,2}time_{0,2}$', re.IGNORECASE),
    'dPdtime': re.compile(r'^_{0,2}d_{0,2}p_{0,2}d_{0,2}time_{0,2}$', re.IGNORECASE),
    'dPdu': re.compile(r'^_{0,2}d_{0,2}p_{0,2}d_{0,2}u_{0,2}$', re.IGNORECASE),
    'dPdv': re.compile(r'^_{0,2}d_{0,2}p_{0,2}d_{0,2}v_{0,2}$', re.IGNORECASE),
    'dPdw': re.compile(r'^_{0,2}d_{0,2}p_{0,2}d_{0,2}w_{0,2}$', re.IGNORECASE),
    'du': re.compile(r'^_{0,2}d_{0,2}u_{0,2}$', re.IGNORECASE),
    'dv': re.compile(r'^_{0,2}d_{0,2}v_{0,2}$', re.IGNORECASE),
    'dw': re.compile(r'^_{0,2}d_{0,2}w_{0,2}$', re.IGNORECASE),
    #'id': re.compile(r'^_{0,2}id_{0,2}$', re.IGNORECASE),
    'incidentRayRadius': re.compile(r'^_{0,2}incident_{0,2}ray_{0,2}radius_{0,2}$', re.IGNORECASE),
    'incidentRaySpread': re.compile(r'^_{0,2}incident_{0,2}ray_{0,2}spread_{0,2}$', re.IGNORECASE),
    'motionBack': re.compile(r'^_{0,2}motion_{0,2}back_{0,2}$', re.IGNORECASE),
    'motionFore': re.compile(r'^_{0,2}motion_{0,2}fore_{0,2}$', re.IGNORECASE),
    'mpSize': re.compile(r'^_{0,2}mp_{0,2}size_{0,2}$', re.IGNORECASE),
    'outsideIOR': re.compile(r'^_{0,2}outside_{0,2}ior_{0,2}$', re.IGNORECASE),
    'rawId': re.compile(r'^_{0,2}raw_{0,2}id_{0,2}$', re.IGNORECASE),
    'sampleCount': re.compile(r'^_{0,2}sample_{0,2}count_{0,2}$', re.IGNORECASE),
    'time': re.compile(r'^_{0,2}time_{0,2}$', re.IGNORECASE),
    'u': re.compile(r'^_{0,2}u_{0,2}$', re.IGNORECASE),
    'v': re.compile(r'^_{0,2}v_{0,2}$', re.IGNORECASE),
    'w': re.compile(r'^_{0,2}w_{0,2}$', re.IGNORECASE),
}

VRAY_MATERIALS = {
    'Albedo': re.compile(r'^_{0,2}albedo_{0,2}$', re.IGNORECASE),
    'Diffuse': re.compile(r'^_{0,2}diffuse_{0,2}$', re.IGNORECASE),
    'Diffuse_Direct': re.compile(r'^_{0,2}(?:diffuse_{0,2}direct|direct_{0,2}diffuse)_{0,2}$', re.IGNORECASE),
    'Diffuse_Indirect': re.compile(r'^_{0,2}(?:diffuse_{0,2}indirect|indirect_{0,2}diffuse)_{0,2}$', re.IGNORECASE),
    'SSS': re.compile(r'^_{0,2}sss_{0,2}$', re.IGNORECASE),
    'Albedo_SSS': re.compile(r'^_{0,2}(?:albedo_{0,2}sss|sss_{0,2}albedo)_{0,2}$', re.IGNORECASE),
    'SSS_Direct': re.compile(r'^_{0,2}(?:sss_{0,2}direct|direct_{0,2}sss)_{0,2}$', re.IGNORECASE),
    'SSS_Indirect': re.compile(r'^_{0,2}(?:sss_{0,2}indirect|indirect_{0,2}sss)_{0,2}$', re.IGNORECASE),
    'Specular': re.compile(r'^_{0,2}specular_{0,2}$', re.IGNORECASE),
    'Specular_Direct': re.compile(r'^_{0,2}(?:specular_{0,2}direct|direct_{0,2}specular)_{0,2}$', re.IGNORECASE),
    'Specular_Indirect': re.compile(r'^_{0,2}(?:specular_{0,2}indirect|indirect_{0,2}specular)_{0,2}$', re.IGNORECASE),
    'Reflection': re.compile(r'^_{0,2}reflection_{0,2}$', re.IGNORECASE),
    'Reflection_Filter': re.compile(r'^_{0,2}reflection_{0,2}filter_{0,2}$', re.IGNORECASE),
    'Raw_Reflection': re.compile(r'^_{0,2}raw_{0,2}reflection_{0,2}$', re.IGNORECASE),
    'Coat': re.compile(r'^_{0,2}coat_{0,2}$', re.IGNORECASE),
    'Coat_Filter': re.compile(r'^_{0,2}coat_{0,2}filter_{0,2}$', re.IGNORECASE),
    'Raw_Coat_Filter': re.compile(r'^_{0,2}raw_{0,2}coat_{0,2}filter_{0,2}$', re.IGNORECASE),
    'Coat_Reflection': re.compile(r'^_{0,2}coat_{0,2}reflection_{0,2}$', re.IGNORECASE),
    'Raw_Coat_Reflection': re.compile(r'^_{0,2}raw_{0,2}coat_{0,2}reflection_{0,2}$', re.IGNORECASE),
    'Sheen': re.compile(r'^_{0,2}sheen_{0,2}$', re.IGNORECASE),
    'Sheen_Filter': re.compile(r'^_{0,2}sheen_{0,2}filter_{0,2}$', re.IGNORECASE),
    'Raw_Sheen_Filter': re.compile(r'^_{0,2}raw_{0,2}sheen_{0,2}filter_{0,2}$', re.IGNORECASE),
    'Sheen_Reflection': re.compile(r'^_{0,2}sheen_{0,2}reflection_{0,2}$', re.IGNORECASE),
    'Raw_Sheen_Reflection': re.compile(r'^_{0,2}raw_{0,2}sheen_{0,2}reflection_{0,2}$', re.IGNORECASE),
    'Refraction': re.compile(r'^_{0,2}refraction_{0,2}$', re.IGNORECASE),
    'Refraction_Filter': re.compile(r'^_{0,2}refraction_{0,2}filter_{0,2}$', re.IGNORECASE),
    'Raw_Refraction': re.compile(r'^_{0,2}raw_{0,2}refraction_{0,2}$', re.IGNORECASE),
    'Caustics': re.compile(r'^_{0,2}caustics_{0,2}$', re.IGNORECASE),
    'Emission': re.compile(r'^_{0,2}emission_{0,2}$', re.IGNORECASE),
    'Emission_Direct': re.compile(r'^_{0,2}(?:emission_{0,2}direct|direct_{0,2}emission)_{0,2}$', re.IGNORECASE),
    'Emission_Indirect': re.compile(r'^_{0,2}(?:emission_{0,2}indirect|indirect_{0,2}emission)_{0,2}$', re.IGNORECASE),
    'Volume': re.compile(r'^_{0,2}volume_{0,2}$', re.IGNORECASE),
    'Volume_Albedo': re.compile(r'^_{0,2}(?:volume_{0,2}albedo|albedo_{0,2}volume)_{0,2}$', re.IGNORECASE),
    'Volume_Direct': re.compile(r'^_{0,2}(?:volume_{0,2}direct|direct_{0,2}volume)_{0,2}$', re.IGNORECASE),
    'Volume_Indirect': re.compile(r'^_{0,2}(?:volume_{0,2}indirect|indirect_{0,2}volume)_{0,2}$', re.IGNORECASE),
    #'Lighting': re.compile(r'^_{0,2}lighting_{0,2}$', re.IGNORECASE),
    #'Raw_Lighting': re.compile(r'^_{0,2}raw_{0,2}lighting_{0,2}$', re.IGNORECASE),
    #'GI': re.compile(r'^_{0,2}GI_{0,2}$', re.IGNORECASE),
    #'Raw_GI': re.compile(r'^_{0,2}raw_{0,2}GI_{0,2}$', re.IGNORECASE),
    #'Self_Illumination': re.compile(r'^_{0,2}self_{0,2}illum(?:ination)?_{0,2}$', re.IGNORECASE),
    #'Atmospheric_Effects': re.compile(r'^_{0,2}(?:atmospheric_{0,2}effects|atmosphere)_{0,2}$', re.IGNORECASE),
    #'Background': re.compile(r'^_{0,2}background_{0,2}$', re.IGNORECASE),
    #'Shadow': re.compile(r'^_{0,2}shadow_{0,2}$', re.IGNORECASE),
    #'Raw_Shadow': re.compile(r'^_{0,2}raw_{0,2}shadow_{0,2}$', re.IGNORECASE),
    #'Toon': re.compile(r'^_{0,2}toon_{0,2}$', re.IGNORECASE),
}

VRAY_UTILITIES = {
    'alpha': re.compile(r'^_{0,2}(?:alpha|A)_{0,2}$', re.IGNORECASE),
    'rgba': re.compile(r'^_{0,2}rgba_{0,2}$', re.IGNORECASE),
    'Z_Depth': re.compile(r'^_{0,2}(?:z_{0,2}depth|depth_{0,2}z|_{0,2}depth|_{0,2}Z)_{0,2}$', re.IGNORECASE),
    'P': re.compile(r'^_{0,2}(?:p|pos(?:ition)?)_{0,2}$', re.IGNORECASE),
    'P_Camera': re.compile(r'^_{0,2}(?:p|pos(?:ition)?)_{0,2}cam(?:era)?_{0,2}$', re.IGNORECASE),
    'P_Ref': re.compile(r'^_{0,2}p_{0,2}ref(?:erence)?_{0,2}$', re.IGNORECASE),
    'Normals': re.compile(r'^_{0,2}normals?_{0,2}$', re.IGNORECASE),
    'Bump_Normals': re.compile(r'^_{0,2}bump_{0,2}normals?_{0,2}$', re.IGNORECASE),
    'Multi_Matte': re.compile(r'^_{0,2}multi_{0,2}matte_{0,2}$', re.IGNORECASE),
    'Object_Select': re.compile(r'^_{0,2}object_{0,2}select_{0,2}$', re.IGNORECASE),
    'Object_Select_Filter': re.compile(r'^_{0,2}object_{0,2}select_{0,2}filter_{0,2}$', re.IGNORECASE),
    'Material_ID': re.compile(r'^_{0,2}material_{0,2}id_{0,2}$', re.IGNORECASE),
    'Matte_Shadow': re.compile(r'^_{0,2}matte_{0,2}shadow_{0,2}$', re.IGNORECASE),
    'Velocity': re.compile(r'^_{0,2}velocity_{0,2}$', re.IGNORECASE),
    'UVs': re.compile(r'^_{0,2}uvs?_{0,2}$', re.IGNORECASE),
    'other': re.compile(r'^_{0,2}other_{0,2}$', re.IGNORECASE),
    'Extra_Tex': re.compile(r'^_{0,2}extra_{0,2}tex_{0,2}$', re.IGNORECASE),
    'DR_Bucket': re.compile(r'^_{0,2}dr_{0,2}bucket_{0,2}$', re.IGNORECASE),
    'sample': re.compile(r'^_{0,2}sample_{0,2}$', re.IGNORECASE),
    'Sample_Rate': re.compile(r'^_{0,2}sample_{0,2}rate_{0,2}$', re.IGNORECASE),
}

GENERIC_MATERIALS = {
    ## albedo
    'albedo': re.compile(r'^_{0,2}albedo_{0,2}$', re.IGNORECASE),
    ## diffuse
    'diffuse_albedo': re.compile(r'^_{0,2}(?:diffuse_{0,2}albedo|albedo_{0,2}diffuse)_{0,2}$', re.IGNORECASE),
    'diffuse': re.compile(r'^_{0,2}diffuse_{0,2}$', re.IGNORECASE),
    'diffuse_direct': re.compile(r'^_{0,2}(?:diffuse_{0,2}direct|direct_{0,2}diffuse)_{0,2}$', re.IGNORECASE),
    'diffuse_indirect': re.compile(r'^_{0,2}(?:diffuse_{0,2}indirect|indirect_{0,2}diffuse)_{0,2}$', re.IGNORECASE),
    ## sss
    'sss': re.compile(r'^_{0,2}sss_{0,2}$', re.IGNORECASE),
    'sss_albedo': re.compile(r'^_{0,2}(?:sss_{0,2}albedo|albedo_{0,2}sss)_{0,2}$', re.IGNORECASE),
    'sss_direct': re.compile(r'^_{0,2}(?:sss_{0,2}direct|direct_{0,2}sss)_{0,2}$', re.IGNORECASE),
    'sss_indirect': re.compile(r'^_{0,2}(?:sss_{0,2}indirect|indirect_{0,2}sss)_{0,2}$', re.IGNORECASE),
    ## specular
    'specular': re.compile(r'^_{0,2}specular_{0,2}$', re.IGNORECASE),
    'specular_albedo': re.compile(r'^_{0,2}(?:specular_{0,2}albedo|albedo_{0,2}specular)_{0,2}$', re.IGNORECASE),
    'specular_direct': re.compile(r'^_{0,2}(?:specular_{0,2}direct|direct_{0,2}specular)_{0,2}$', re.IGNORECASE),
    'specular_indirect': re.compile(r'^_{0,2}(?:specular_{0,2}indirect|indirect_{0,2}specular)_{0,2}$', re.IGNORECASE),
    ## reflection
    'reflection': re.compile(r'^_{0,2}reflect(?:ion)?_{0,2}$', re.IGNORECASE),
    'reflection_direct': re.compile(r'^_{0,2}(?:reflect(?:ion)?_{0,2}direct|direct_{0,2}reflect(?:ion)?)_{0,2}$', re.IGNORECASE),
    'reflection_indirect': re.compile(r'^_{0,2}(?:reflect(?:ion)?_{0,2}indirect|indirect_{0,2}reflect(?:ion)?)_{0,2}$', re.IGNORECASE),
    ## refraction
    'refraction': re.compile(r'^_{0,2}refract(?:ion)?_{0,2}$', re.IGNORECASE),
    ## coat
    'coat': re.compile(r'^_{0,2}coat_{0,2}$', re.IGNORECASE),
    'coat_albedo': re.compile(r'^_{0,2}(?:coat_{0,2}albedo|albedo_{0,2}coat)_{0,2}$', re.IGNORECASE),
    'coat_direct': re.compile(r'^_{0,2}(?:coat_{0,2}direct|direct_{0,2}coat)_{0,2}$', re.IGNORECASE),
    'coat_indirect': re.compile(r'^_{0,2}(?:coat_{0,2}indirect|indirect_{0,2}coat)_{0,2}$', re.IGNORECASE),
    ## sheen
    'sheen': re.compile(r'^_{0,2}sheen_{0,2}$', re.IGNORECASE),
    'sheen_albedo': re.compile(r'^_{0,2}(?:sheen_{0,2}albedo|albedo_{0,2}sheen)_{0,2}$', re.IGNORECASE),
    'sheen_direct': re.compile(r'^_{0,2}(?:sheen_{0,2}direct|direct_{0,2}sheen)_{0,2}$', re.IGNORECASE),
    'sheen_indirect': re.compile(r'^_{0,2}(?:sheen_{0,2}indirect|indirect_{0,2}sheen)_{0,2}$', re.IGNORECASE),
    ## transmission
    'transmission': re.compile(r'^_{0,2}transmission_{0,2}$', re.IGNORECASE),
    'transmission_albedo': re.compile(r'^_{0,2}(?:transmission_{0,2}albedo|albedo_{0,2}transmission)_{0,2}$', re.IGNORECASE),
    'transmission_direct': re.compile(r'^_{0,2}(?:transmission_{0,2}direct|direct_{0,2}transmission)_{0,2}$', re.IGNORECASE),
    'transmission_indirect': re.compile(r'^_{0,2}(?:transmission_{0,2}indirect|indirect_{0,2}transmission)_{0,2}$', re.IGNORECASE),
    ## emission
    'emission': re.compile(r'^_{0,2}emission_{0,2}$', re.IGNORECASE),
    'emission_direct': re.compile(r'^_{0,2}(?:emission_{0,2}direct|direct_{0,2}emission)_{0,2}$', re.IGNORECASE),
    'emission_indirect': re.compile(r'^_{0,2}(?:emission_{0,2}indirect|indirect_{0,2}emission)_{0,2}$', re.IGNORECASE),
    ## volume
    'volume': re.compile(r'^_{0,2}volume_{0,2}$', re.IGNORECASE),
    'volume_albedo': re.compile(r'^_{0,2}(?:volume_{0,2}albedo|albedo_{0,2}volume)_{0,2}$', re.IGNORECASE),
    'volume_direct': re.compile(r'^_{0,2}(?:volume_{0,2}direct|direct_{0,2}volume)_{0,2}$', re.IGNORECASE),
    'volume_indirect': re.compile(r'^_{0,2}(?:volume_{0,2}indirect|indirect_{0,2}volume)_{0,2}$', re.IGNORECASE),
}

GENERIC_UTILITIES = {
    'alpha': re.compile(r'^_{0,2}(?:alpha_{0,2}|A)_{0,2}$', re.IGNORECASE),
    'rgba': re.compile(r'^_{0,2}rgba_{0,2}$', re.IGNORECASE),
    'z_depth': re.compile(r'^_{0,2}(?:z_{0,2}depth|depth_{0,2}z|depth_{0,2}extra|depth|Z)_{0,2}$', re.IGNORECASE),
    'P': re.compile(r'^_{0,2}(?:p(?:os(?:ition)?)?_{0,2}[a-z]+|p(?:os(?:ition)?)?)_{0,2}$', re.IGNORECASE),
    'p_camera': re.compile(r'^_{0,2}(?:p(?:os(?:ition)?)?_{0,2}cam(?:era)?_{0,2}[a-z]+|p(?:os(?:ition)?)?_{0,2}cam(?:era)?)_{0,2}$', re.IGNORECASE),
    'p_ref': re.compile(r'^_{0,2}(?:p(?:os(?:ition)?)?_{0,2}ref(?:erence)?_{0,2}[a-z]+|p(?:os(?:ition)?)?_{0,2}ref(?:erence)?)_{0,2}$', re.IGNORECASE),
    'p_object': re.compile(r'^_{0,2}(?:p(?:os(?:ition)?)?_{0,2}obj(?:ect)?_{0,2}[a-z]+|p(?:os(?:ition)?)?_{0,2}obj(?:ect)?)_{0,2}$', re.IGNORECASE),
    'p_world': re.compile(r'^_{0,2}(?:p(?:os(?:ition)?)?_{0,2}world_{0,2}[a-z]+|p(?:os(?:ition)?)?_{0,2}world)_{0,2}$', re.IGNORECASE),
    'N': re.compile(r'^_{0,2}(?:n(?:orm(?:als?)?)?_{0,2}[a-z]+|n(?:orm(?:als?)?)?)_{0,2}$', re.IGNORECASE),
    'n_camera': re.compile(r'^_{0,2}(?:n(?:orm(?:als?)?)?_{0,2}cam(?:era)?_{0,2}[a-z]+|n(?:orm(?:als?)?)?_{0,2}cam(?:era)?)_{0,2}$', re.IGNORECASE),
    'n_object': re.compile(r'^_{0,2}(?:n(?:orm(?:als?)?)?_{0,2}obj(?:ect)?_{0,2}[a-z]+|n(?:orm(?:als?)?)?_{0,2}obj(?:ect)?)_{0,2}$', re.IGNORECASE),
    'n_world': re.compile(r'^_{0,2}(?:n(?:orm(?:als?)?)?_{0,2}world_{0,2}[a-z]+|n(?:orm(?:als?)?)?_{0,2}world)_{0,2}$', re.IGNORECASE),
    'n_bump': re.compile(r'^_{0,2}(?:n(?:orm(?:als?)?)?_{0,2}bump_{0,2}[a-z]+|bump_{0,2}n(?:orm(?:als?)?)?_{0,2}[a-z]+|n(?:orm(?:als?)?)?_{0,2}bump|bump_{0,2}n(?:orm(?:als?)?)?)_{0,2}$', re.IGNORECASE),
    'ID': re.compile(r'^_{0,2}ID(?:_{0,2}[a-z0-9]+)*_{0,2}$', re.IGNORECASE),
    'mask': re.compile(r'^_{0,2}mask(?:_{0,2}[a-z0-9]+)*_{0,2}$', re.IGNORECASE),
    'matte': re.compile(r'^_{0,2}matte(?:_{0,2}[a-z0-9]+)*_{0,2}$', re.IGNORECASE),
    'matteID': re.compile(r'^_{0,2}matte_{0,2}id_{0,2}[0-9]{1,3}_{0,2}$', re.IGNORECASE),
    'motionvectors': re.compile(r'^_{0,2}motion_{0,2}vectors?_{0,2}$', re.IGNORECASE),
    'velocity': re.compile(r'^_{0,2}(?:vel(?:ocity)?)?_{0,2}$', re.IGNORECASE),
}

def combine_with_generics(engine_data, generic_data):
    '''Combines engine specific lists/dicts with generic dicts while preserving UI order'''
    combined = collections.OrderedDict()

    if isinstance(engine_data, list):
        for item in engine_data:
            combined[item] = None
    elif isinstance(engine_data, dict):
        for k, v in engine_data.items():
            combined[k] = v

    for k, v in generic_data.items():
        if k not in combined:
            combined[k] = v

    return combined

## render engine dictionaries
ADDITIONAL_LIGHTING_AOVS = {
    'Generic': GENERIC_ADDITIONAL_LIGHTING,
    'Arnold': combine_with_generics(ARNOLD_ADDITIONAL_LIGHTING, GENERIC_ADDITIONAL_LIGHTING),
    'Karma': combine_with_generics(KARMA_ADDITIONAL_LIGHTING, GENERIC_ADDITIONAL_LIGHTING),
    #'Redshift': ,
    'RenderMan': combine_with_generics(RENDERMAN_ADDITIONAL_LIGHTING, GENERIC_ADDITIONAL_LIGHTING),
    'V-Ray': combine_with_generics(VRAY_ADDITIONAL_LIGHTING, GENERIC_ADDITIONAL_LIGHTING),
}

MATERIAL_AOVS = {
    'Generic': GENERIC_MATERIALS,
    'Arnold': combine_with_generics(ARNOLD_MATERIALS, GENERIC_MATERIALS),
    'Karma': combine_with_generics(KARMA_MATERIALS, GENERIC_MATERIALS),
    #'Redshift': ,
    'RenderMan': combine_with_generics(RENDERMAN_MATERIALS, GENERIC_MATERIALS),
    'V-Ray': combine_with_generics(VRAY_MATERIALS, GENERIC_MATERIALS),
}

UTILITY_AOVS = {
    'Generic': GENERIC_UTILITIES,
    'Arnold': combine_with_generics(ARNOLD_UTILITIES, GENERIC_UTILITIES),
    'Karma': combine_with_generics(KARMA_UTILITIES, GENERIC_UTILITIES),
    #'Redshift': ,
    'RenderMan': combine_with_generics(RENDERMAN_UTILITIES, GENERIC_UTILITIES),
    'V-Ray': combine_with_generics(VRAY_UTILITIES, GENERIC_UTILITIES),
}

X_SPACE = 300

Y_SPACE = 100

MERGE_FROM_COLOUR = 2569876223

MERGE_PLUS_COLOUR = 2197786623

DEFAULT_SETTINGS = {'rebuild_mode': 'Additive',
                    'breakout_materials': True,
                    'breakout_lightgroups': True,
                    'breakout_utilities': True,
                    'lg_regex' : LIGHTGROUP_REGEX,
                    'additional_lighting': ADDITIONAL_LIGHTING_AOVS['Generic'],
                    'expected_materials': MATERIAL_AOVS['Generic'],
                    'expected_utilities': UTILITY_AOVS['Generic'],
                    'x_space': X_SPACE,
                    'y_space': Y_SPACE}

## nodegraph helper functions
def get_centre_xypos(node):
    '''Returns a tuple with the xpos and ypos of `node` factoring the node width to obtain the node's center point.'''
    xpos = int (node.xpos() + node.screenWidth()/2 )
    ypos = int (node.ypos()  + node.screenHeight()/2 )
    return xpos, ypos

def set_centred_xypos(node, xpos, ypos):
    '''Positions `node` at the `xpos and `ypos` position in the nodegraph,
    factoring the node width to obtain the node's center point.'''
    x_centred = int (xpos - node.screenWidth()/2)
    y_centred = int (ypos - node.screenHeight()/2)
    node.setXYpos(x_centred, y_centred)

## layer utility functions
def get_all_layers(node):
    '''returns a list of all the layers in a node '''
    channels = node.channels()
    layers = list(set([c.split('.')[0] for c in channels ]))
    layers.sort()
    #print (layers) ## for debugging
    return layers

def get_lightgroup_layers(node, lightgroup_regex=LIGHTGROUP_REGEX, additional_lighting=ADDITIONAL_LIGHTING_AOVS, exclude=None):
    '''Return a list of all aovs in node which are lightgroups, excluding any AOVs explicitly in the exclude list (e.g. user-moved materials).'''
    exclude_lower = {e.lower() for e in (exclude or [])}
    lightgroups_or_materials = []
    for layer in get_all_layers(node):
        if layer.lower() in exclude_lower:
            continue
        result = lightgroup_regex.search(layer)
        if result:
            lightgroups_or_materials.append(layer)
        elif layer in additional_lighting:
            lightgroups_or_materials.append(layer)
    return lightgroups_or_materials

def get_materials(node, expected_materials):
    '''Returns a list of all aovs which match the expected_materials list, using strict regex if defined.'''
    materials = []
    all_layers = get_all_layers(node)

    ## build a master regex lookup from all engine configurations
    regex_map = {}
    for engine_name, config in MATERIAL_AOVS.items():
        if isinstance(config, dict):
            for key, val in config.items():
                if val and hasattr(val, 'search'):
                    regex_map[key] = val

    for material in expected_materials:
        regex = regex_map.get(material)

        for layer in all_layers:
            if layer in materials:
                continue  ## prevent duplicates

            if regex:
                ## strict match to prevent substring overlaps (e.g. 'albedo' catching 'volume_albedo')
                match = regex.match(layer)
                if match and match.group() == layer:
                    materials.append(layer)
            else:
                ## fallback to exact case-insensitive match
                if layer.lower() == material.lower():
                    materials.append(layer)

    return materials

def get_utilities(node, expected_utilities):
    '''Returns a list of all aovs which match the expected_utilities list, using strict regex if defined.'''
    utilities = []
    all_layers = get_all_layers(node)

    ## build a master regex lookup from all engine configurations
    regex_map = {}
    for engine_name, config in UTILITY_AOVS.items():
        if isinstance(config, dict):
            for key, val in config.items():
                if val and hasattr(val, 'search'):
                    regex_map[key] = val

    for utility in expected_utilities:
        regex = regex_map.get(utility)

        for layer in all_layers:
            if layer in utilities:
                continue  ## prevent duplicates

            if regex:
                ## strict match to prevent substring overlaps (e.g. 'alpha' catching 'diffuse_alpha')
                match = regex.match(layer)
                if match and match.group() == layer:
                    utilities.append(layer)
            else:
                ## fallback to exact case-insensitive match
                if layer.lower() == utility.lower():
                    utilities.append(layer)

    return utilities

def validate_duplicates(p, multiline_to_list, mode):
    '''Check for duplicate AOVs within and across editable columns.
    Returns a list of error message strings, and a dictionary of warnings, empty if clean.'''

    def clean_input(knob_value):
        raw = multiline_to_list(knob_value)
        return [l for l in raw if ":" not in l and "---" not in l and l.strip()]

    columns = {
        'AOVS READ': clean_input(p.aov_read.value()),
        'UNASSIGNED READ': clean_input(p.aov_unassigned_read.value()),
        'ADDITIONAL LIGHTING': clean_input(p.additional_lighting.value()),
        'MATERIALS': clean_input(p.materials.value()),
        'UTILITIES': clean_input(p.utilities.value()),
        'OMIT': clean_input(p.omit_list.value()),
    }

    ## each frozenset defines one permitted overlap pair. overlaps are permitted between one "Read" source and one destination column.
    ALLOWED_OVERLAP = {
        ## Overlaps with UNASSIGNED READ
        frozenset({'UNASSIGNED READ', 'ADDITIONAL LIGHTING'}),
        frozenset({'UNASSIGNED READ', 'MATERIALS'}),
        frozenset({'UNASSIGNED READ', 'UTILITIES'}),
        frozenset({'UNASSIGNED READ', 'OMIT'}),

        ## Overlaps with AOVS READ
        frozenset({'AOVS READ', 'ADDITIONAL LIGHTING'}),
        frozenset({'AOVS READ', 'UTILITIES'}),
        frozenset({'AOVS READ', 'OMIT'}),
    }

    ## Combinations that will trigger a user prompt on an Additive rebuild
    WARNING_OVERLAP = {
        frozenset({'AOVS READ', 'MATERIALS'}),
        frozenset({'ADDITIONAL LIGHTING', 'MATERIALS'})
    }

    errors = []
    warnings = {}

    ## intra-column duplicates (unchanged)
    for col_name, aovs in columns.items():
        seen = set()
        reported = set()
        for aov in aovs:
            if aov in seen and aov not in reported:
                errors.append(
                    "Duplicate '%s' AOV found in column %s.\n"
                    "Please amend. Duplicate AOVs can break the rebuild."
                    % (aov, col_name)
                )
                reported.add(aov)
            seen.add(aov)

    ## inter-column duplicates
    aov_to_cols = {}
    for col_name, aovs in columns.items():
        for aov in set(aovs):
            aov_to_cols.setdefault(aov, []).append(col_name)

    for aov, cols in sorted(aov_to_cols.items()):
        if len(cols) > 1:
            col_set = frozenset(cols)
            ## skip only if the exact set of offending columns is a subset of one of the permitted pairs
            if any(col_set <= pair for pair in ALLOWED_OVERLAP):
                continue

            ## If Additive mode, filter into the warnings dictionary
            if mode == 'Additive' and any(col_set <= pair for pair in WARNING_OVERLAP):
                col_key = tuple(cols)
                warnings.setdefault(col_key, []).append(aov)
                continue

            errors.append(
                "'%s' AOV found in multiple columns: %s.\n"
                "Please amend. Duplicate AOVs can break the rebuild."
                % (aov, ', '.join(cols))
            )

    return errors, warnings

## user config functions
def setup_breakout_panel(node=None):
    if not node:
        node = nuke.selectedNode()

    def multiline_to_list(knob_value):
        return [line.strip() for line in knob_value.split('\n') if line.strip()]

    class BreakoutPanel(nukescripts.PythonPanel):
        def __init__(self, node):
            nukescripts.PythonPanel.__init__(self, "AOV Rebuild")
            self.setMinimumSize(1700, 1180)
            self.node = node
            self._read_user_edited = False

            ## column rebuild mode
            self.addKnob(nuke.Text_Knob('', '<center><b>Rebuild Mode</b><center>'))
            self.addKnob(nuke.Text_Knob("column_rebuild_mode_spacer_01", "", " " * 20))
            self.rebuild_mode = nuke.Enumeration_Knob('rebuild_mode', 'Rebuild:', ['Additive', 'Subtractive'])
            self.rebuild_mode.setTooltip("Choose between a Additive or Subtractive rebuild")
            self.addKnob(self.rebuild_mode)
            self.addKnob(nuke.Text_Knob("column_rebuild_mode_spacer_02", "", " " * 20))

            ## column render engine
            self.addKnob(nuke.Text_Knob('', '<center><b>Render Engine</b><center>'))
            self.addKnob(nuke.Text_Knob("column_render_engine_spacer_01", "", " " * 20))
            self.render_engine = nuke.Enumeration_Knob('render_engine', 'Render Engine:', ['Generic', 'Arnold', 'Karma', 'RenderMan', 'V-Ray'])
            self.render_engine.setTooltip("Choose the render naming convention.\n\nGeneric uses regex of common use case AOV names.\n\nArnold, Karma, Renderman, V-Ray options combine the generic regex with naming conventions specific to the corresponding render engine.")
            self.addKnob(self.render_engine)
            ## get the initial engine value
            engine = self.render_engine.value()
            self.addKnob(nuke.Text_Knob("column_render_engine_spacer_02", "", " " * 20))

            ## column regex settings
            self.addKnob(nuke.Text_Knob('', '<center><b>Lightgroup Settings</b><center>'))
            self.addKnob(nuke.Text_Knob("column_regex_settings_01", "", " " * 20))

            ## the regex string field (linked to LIGHTGROUP_REGEX by default)
            self.lg_regex = nuke.String_Knob('lg_regex', 'Lightgroup Regex', LIGHTGROUP_REGEX.pattern)
            self.lg_regex.setTooltip("Enter a regex to match your Lightgroup naming convention.\n\nFor help to match your Lightgroup naming convention visit\n\nhttps://regex101.com\n\nNote: After editing mouse click outside of the dialog box to see updates in AOV Management")
            self.lg_regex.setEnabled(False)  ## read only by default
            self.addKnob(self.lg_regex)

            ## edit toggle
            self.edit_regex = nuke.Boolean_Knob('edit_regex', 'Edit regex')
            self.addKnob(self.edit_regex)

            self.ignore_case = nuke.Boolean_Knob('ignore_case', 'Ignore case for regex')
            self.ignore_case.setValue(True)
            self.addKnob(self.ignore_case)

            ## column aov management
            self.addKnob(nuke.Text_Knob('column_aov_management_spacer_01', '', ' '))
            self.addKnob(nuke.Text_Knob('', '<center><b>AOV Management</b><center>'))
            self.addKnob(nuke.Text_Knob("column_aov_management_spacer_02", "", " " * 20))

            ## row of multiline knobs
            self.aov_read = nuke.Multiline_Eval_String_Knob('aov_read', '', '')
            self.aov_read.setEnabled(False)
            self.aov_read.setTooltip("Lists LIGHT, MATERIAL & UTILITY AOVs found in the render.\n\nThis column is read only to see assigned AOVs that match the corresponding list. It is editable by checking the 'Edit AOVs Read' button below.\n\nAOVs must be added 1 per line.\n\nIf you cannot see AOVs you wish to populate in aov_read\n\nyou can update the Render Engine.\n\ncut / paste from UNASSIGNED READ:\n\nor update... 'Lightgroup Regex'\n\nto re-populate this column.")

            self.aov_unassigned_read = nuke.Multiline_Eval_String_Knob('aov_unassigned_read', '', '')
            self.aov_unassigned_read.setEnabled(True)
            self.aov_unassigned_read.setTooltip("Lists UNASSIGNED AOVs found in the render.\n\nAOVs listed under UNASSIGNED READ: can be cut to columns\n\nADD LIGHTING:\n\nADD MATERIALS:\n\nADD UTILITIES:\n\nOMIT: (as per user preference for breakout or omission).\n\nAOVs added to these lists must be added 1 per line.")

            ## fetch all layers to filter lists dynamically
            all_layers = get_all_layers(self.node)
            ## scan all EXR layers against the compiled regex patterns in the dictionary
            valid_additional_lighting = [layer for layer in all_layers if any(pattern and pattern.match(layer) for pattern in ADDITIONAL_LIGHTING_AOVS.get(engine, {}).values())]

            self.additional_lighting = nuke.Multiline_Eval_String_Knob('additional_lighting', '', '\n'.join(valid_additional_lighting))
            self.additional_lighting.setTooltip("Add custom or unassigned light AOVs found in the render to the 'Lightgroup' breakout by adding them to this list.\n\nAOVs must be added 1 per line.\n\nCustom or unassigned lights are typically listed under\n\nUNASSIGNED READ:\n\nin the previous (aov_unassigned_read) column.")

            self.materials = nuke.Multiline_Eval_String_Knob('materials', '')
            self.materials.setTooltip("Add custom materials found in the render to the 'Materials' breakout by adding to this list.\n\nAOVs must be added 1 per line.")

            self.utilities = nuke.Multiline_Eval_String_Knob('utilities', '')
            self.utilities.setTooltip("Add custom utilities found in the render to the 'Utilities' breakout by adding to this list.\n\nAOVs must be added 1 per line.")

            crypto_layers = [layer for layer in all_layers if 'crypto' in layer.lower()]
            initial_omit_list = '\n'.join(crypto_layers)

            self.omit_list = nuke.Multiline_Eval_String_Knob('omit_list', '', initial_omit_list)
            self.omit_list.setTooltip("Is where users can add AOVs from previous columns they wish to omit from the breakout.\n\nAOVs must be added 1 per line.\n\nCryptomatte layers are added to the omit list by default.")

            ## clear startlines for knobs 2 through 6 to keep them on the same row
            for k in [self.aov_unassigned_read, self.additional_lighting, self.materials, self.utilities, self.omit_list]: k.clearFlag(nuke.STARTLINE)

            self.addKnob(self.aov_read)
            self.addKnob(self.aov_unassigned_read)
            self.addKnob(self.additional_lighting)
            self.addKnob(self.materials)
            self.addKnob(self.utilities)
            self.addKnob(self.omit_list)

            ## toggle for AOVS READ column
            self.edit_read = nuke.Boolean_Knob('edit_read', 'Edit AOVs Read')
            #self.addKnob(nuke.Text_Knob("toggle_for_AOVS_READ_column_spacer_01", "", " " * 40))
            self.addKnob(nuke.Text_Knob("toggle_for_AOVS_READ_column_spacer_02", "", " " * 20))
            self.edit_read.setTooltip("Enable this to edit the 'AOVS READ' column.")
            self.addKnob(self.edit_read)
            self.addKnob(nuke.Text_Knob("toggle_for_AOVS_READ_column_spacer_03", "", " " * 20))

            ## column breakout options
            self.addKnob(nuke.Text_Knob('', '<center><b>Breakout Options</b><center>'))
            self.addKnob(nuke.Text_Knob("column_breakout_options_spacer_01", "", " " * 20))
            self.breakout_mode = nuke.Enumeration_Knob('breakout_mode', 'Breakout:', ['Materials_&_Lightgroups', 'Materials', 'Lightgroups', 'Utilities'])
            self.breakout_mode.setTooltip("Note: If Utilities is selected 'Breakout Utilities' must still be switched on for utilities to breakout.")
            self.breakout_utilities = nuke.Boolean_Knob('breakout_utilities', 'Breakout Utilities')
            self.breakout_utilities.setValue(True)

            self.addKnob(self.breakout_mode)
            self.addKnob(self.breakout_utilities)

            ## column layout settings
            self.addKnob(nuke.Text_Knob('column_layout_settings_spacer_01', '', ' '))
            self.addKnob(nuke.Text_Knob('', '<center><b>Breakout Layout</b><center>'))
            self.addKnob(nuke.Text_Knob("column_layout_settings_spacer_02", "", " " * 20))
            self.breakout_direction = nuke.Enumeration_Knob('breakout_direction', 'Breakout Direction', ['-X (Left)', '+X (Right)'])
            self.breakout_direction.setTooltip("Choose whether the nodes are built to the left (-x) or right (+x) of the main pipe.")
            self.x_space = nuke.Int_Knob('x_space', 'X space between nodes')
            self.y_space = nuke.Int_Knob('y_space', 'Y space between nodes')
            self.x_space.setValue(X_SPACE)
            self.y_space.setValue(Y_SPACE)
            self.addKnob(self.breakout_direction)
            self.addKnob(self.x_space)
            self.addKnob(self.y_space)
            self.addKnob(nuke.Text_Knob("column_layout_settings_spacer_03", "", " " * 20))

            ## column qc settings
            self.addKnob(nuke.Text_Knob('', '<center><b>Quality Check</b><center>'))
            self.addKnob(nuke.Text_Knob("column_qc_settings_spacer_01", "", " " * 40))
            self.addKnob(nuke.Text_Knob("column_qc_settings_spacer_02", "", " " * 20))
            self.check_unassigned_values_mats = nuke.Boolean_Knob('check_unassigned_values_mats', 'Check for negative values (Materials Unassigned Pipe)')
            self.check_unassigned_values_lights = nuke.Boolean_Knob('check_unassigned_values_lights', 'Check for negative values (Lights Unassigned Pipe)')
            self.addKnob(self.check_unassigned_values_mats)
            self.addKnob(self.check_unassigned_values_lights)
            self.addKnob(nuke.Text_Knob("column_qc_settings_spacer_03", "", " " * 20))

            self.addKnob(nuke.Text_Knob('', '<font color="#575757"><b>v1.1 | David Thomas | 2026</b></font>'))
            self.addKnob(nuke.Text_Knob("title_spacer_02", "", " " * 20))

            ## populate columns
            self.update_aov_list()

        def knobChanged(self, knob):
            '''Manages UI logic and dynamic panel.'''
            if knob == self.render_engine:
                engine = self.render_engine.value()
                all_layers = get_all_layers(self.node)

                ## 1. Force the AOVS READ edit state off
                self._read_user_edited = False
                self.edit_read.setValue(False)
                self.aov_read.setEnabled(False)

                ## 2. Clear user-input columns back to empty defaults
                self.materials.setValue('')
                self.utilities.setValue('')

                ## 3. Reset OMIT list to default (Cryptomatte layers only)
                crypto_layers = [layer for layer in all_layers if 'crypto' in layer.lower()]
                self.omit_list.setValue('\n'.join(crypto_layers))

                ## 4. Reset ADDITIONAL LIGHTING to base engine defaults
                valid_additional_lighting = [layer for layer in all_layers if any(
                    pattern and pattern.match(layer) for pattern in ADDITIONAL_LIGHTING_AOVS.get(engine, {}).values())]
                self.additional_lighting.setValue('\n'.join(valid_additional_lighting))

                ## 5. Refresh the AOVS READ and UNASSIGNED READ columns
                self.update_aov_list()

            elif knob == self.lg_regex or knob == self.ignore_case:
                self._read_user_edited = False
                self.update_aov_list()

            elif knob == self.edit_regex:
                self.lg_regex.setEnabled(self.edit_regex.value())

            ## logic for editing the AOVs read column
            if knob == self.aov_read and self.edit_read.value():
                self._read_user_edited = True
            elif knob == self.edit_read:
                self.aov_read.setEnabled(self.edit_read.value())

        def update_aov_list(self):
            '''Refreshes the Read-Only columns and maintains clean input columns.'''
            flags = re.IGNORECASE if self.ignore_case.value() else 0
            current_regex = re.compile(self.lg_regex.value(), flags)

            def clean_input(knob_value):
                return [line for line in multiline_to_list(knob_value) if
                        ":" not in line and "---" not in line and line.strip()]

            cur_add_light = clean_input(self.additional_lighting.value())
            cur_mats = clean_input(self.materials.value())
            cur_utils = clean_input(self.utilities.value())
            omit_set = set(clean_input(self.omit_list.value()))
            cur_read = clean_input(self.aov_read.value()) if self._read_user_edited else []

            ## create a master set of user overrides so UNASSIGNED READ never shows duplicates
            user_overrides = set(cur_add_light + cur_mats + cur_utils + list(omit_set) + cur_read)

            engine = self.render_engine.value()
            engine_mats = list(MATERIAL_AOVS.get(engine, {}))
            engine_utils = list(UTILITY_AOVS.get(engine, {}))

            lgs = get_lightgroup_layers(self.node, lightgroup_regex=current_regex, additional_lighting=cur_add_light)
            mats = get_materials(self.node, expected_materials=engine_mats + cur_mats)
            utils = get_utilities(self.node, expected_utilities=engine_utils + cur_utils)

            all_layers = get_all_layers(self.node)

            ## dynamically subtract known layers to find 'others'
            known_layers = set(lgs + mats + utils).union(user_overrides)
            others = [l for l in all_layers if l not in known_layers and l != 'rgba']

            ## column 1: AOVS READ
            if not self.edit_read.value() and not self._read_user_edited:
                read_out = []

                lg_section = "LIGHTS READ:\n" + "-" * 20
                exclusion_set = set(mats + utils + others).union(user_overrides)
                valid_lgs = [l for l in lgs if l not in exclusion_set]
                if valid_lgs:
                    lg_section += "\n" + "\n".join(valid_lgs)
                read_out.append(lg_section)

                m_list = [m for m in mats if m not in user_overrides]
                mat_section = "\nMATERIALS READ:\n" + "-" * 25
                if m_list:
                    mat_section += "\n" + "\n".join(m_list)
                read_out.append(mat_section)

                u_list = [u for u in utils if u not in user_overrides]
                util_section = "\nUTILITIES READ:\n" + "-" * 23
                if u_list:
                    util_section += "\n" + "\n".join(u_list)
                read_out.append(util_section)

                self.aov_read.setValue("\n".join(read_out))

            ## column 2: UNASSIGNED READ
            other_out = []
            other_section = "UNASSIGNED READ:\n" + "-" * 28
            if others:
                other_section += "\n" + "\n".join(others)
            other_out.append(other_section)

            self.aov_unassigned_read.setValue("\n".join(other_out))

            ## column 3: ADDITIONAL LIGHTING
            add_out = ["ADD LIGHTING:", "-" * 22]
            if cur_add_light:
                add_out.extend(cur_add_light)
            add_out.append("")
            self.additional_lighting.setValue("\n".join(add_out))

            ## column 4: MATERIALS
            mat_out = ["ADD MATERIALS:", "-" * 24]
            if cur_mats:
                mat_out.extend(cur_mats)
            mat_out.append("")
            self.materials.setValue("\n".join(mat_out))

            ## column 5: UTILITIES
            util_out = ["ADD UTILITIES:", "-" * 21]
            if cur_utils:
                util_out.extend(cur_utils)
            util_out.append("")
            self.utilities.setValue("\n".join(util_out))

            ## column 6: OMIT
            omit_out = ["OMIT:", "-" * 8]
            if omit_set:
                omit_out.extend(sorted(list(omit_set)))
            omit_out.append("")
            self.omit_list.setValue("\n".join(omit_out))

    p = BreakoutPanel(node)
    while True:
        if not p.showModalDialog():
            return None

        mode = p.rebuild_mode.value()
        errors, warnings = validate_duplicates(p, multiline_to_list, mode)

        if errors:
            nuke.message('\n\n'.join(errors))
            continue  ## OK re-opens the panel via the loop

        if warnings:
            proceed = True
            for cols, aovs in warnings.items():
                aov_str = ', '.join(aovs)
                col_str = ', '.join(cols)
                msg = "Warning: Duplicate %s AOVs in columns: %s.\n\nThis is only advisable for Emissive objects.\n\nDo you wish to continue?" % (
                    aov_str, col_str)
                if not nuke.ask(msg):
                    proceed = False
                    break

            if not proceed:
                continue  ## "No" on the prompt re-opens the panel via the loop

        break

    ## settings collection
    settings = DEFAULT_SETTINGS.copy()
    flags = re.IGNORECASE if p.ignore_case.value() else 0
    settings['rebuild_mode'] = p.rebuild_mode.value()
    settings['lg_regex'] = re.compile(p.lg_regex.value(), flags)

    def clean_input(knob_value):
        raw = multiline_to_list(knob_value)
        return [l for l in raw if ":" not in l and "---" not in l and l.strip()]

    engine = p.render_engine.value()
    engine_mats = list(MATERIAL_AOVS.get(engine, {}))
    engine_utils = list(UTILITY_AOVS.get(engine, {}))

    explicit_materials = clean_input(p.materials.value())
    settings['additional_lighting'] = clean_input(p.additional_lighting.value())
    settings['expected_materials'] = engine_mats + explicit_materials
    settings['expected_utilities'] = engine_utils + clean_input(p.utilities.value())
    settings['omit_list'] = clean_input(p.omit_list.value())
    settings['unassigned_list'] = clean_input(p.aov_unassigned_read.value())

    ## If the user manually edited the AOVS READ column, carefully parse out the sections
    if p._read_user_edited:
        custom_lgs = []
        custom_mats = []
        custom_utils = []
        current_section = None

        for line in p.aov_read.value().split('\n'):
            line = line.strip()
            if not line or "---" in line:
                continue
            if line.endswith(':'):
                current_section = line
                continue

            if current_section == 'LIGHTS READ:':
                custom_lgs.append(line)
            elif current_section == 'MATERIALS READ:':
                custom_mats.append(line)
            elif current_section == 'UTILITIES READ:':
                custom_utils.append(line)

        settings['custom_lightgroups'] = custom_lgs

        ## ensure AOVs placed in ADD LIGHTING aren't ignored when the read column is edited
        for add_light in settings['additional_lighting']:
            if add_light not in settings['custom_lightgroups']:
                settings['custom_lightgroups'].append(add_light)

        ## ensure any custom materials/utilities extracted from user edits strictly override expected lists
        settings['expected_materials'] = custom_mats + explicit_materials
        settings['expected_utilities'] = custom_utils + clean_input(p.utilities.value())
    else:
        settings['custom_lightgroups'] = None

    ## any AOV defined in the materials (both hidden engine defaults and manual additions) must be excluded from lightgroup detection
    settings['lg_exclude'] = settings['expected_materials']

    mode = p.breakout_mode.value()
    settings['breakout_materials'] = mode in ('Materials_&_Lightgroups', 'Materials')
    settings['breakout_lightgroups'] = mode in ('Materials_&_Lightgroups', 'Lightgroups')
    settings['breakout_utilities'] = p.breakout_utilities.value()
    settings['x_dir'] = -1 if p.breakout_direction.value() == '-X (Left)' else 1  ## must correspond with self.breakout_direction in layout settings
    settings['x_space'] = int(p.x_space.value())
    settings['y_space'] = int(p.y_space.value())
    settings['check_unassigned_values_mats'] = p.check_unassigned_values_mats.value()
    settings['check_unassigned_values_lights'] = p.check_unassigned_values_lights.value()

    return settings

def custom_breakout_lightgroups_and_materials(node=None):
    '''Obtain custom user settings from a panel and the run the breakout script'''

    ## pre-run warnings: check selection status first
    selected_nodes = nuke.selectedNodes()

    # check if nothing is selected
    if not selected_nodes and not node:
        nuke.message("No node selected. Please select a node.")
        return

    # check if too many nodes are selected
    if len(selected_nodes) > 1:
        nuke.message("Multiple nodes selected. Please select only 1 node.")
        return

    ## assign node if it wasn't passed explicitly
    if not node:
        node = selected_nodes[0]

    ## hard stop if Unpremult or Premult
    if node.Class() in ('Unpremult', 'Premult'):
        nuke.message(
            "Selected node is a %s node.\n\n"
            "Because AOV_rebuild begins by unpremultiplying the RGBA channel, "
            "by appending to a %s node you may break the rebuild.\n\n"
            "Please make sure Premult / Unpremult nodes are not being used upstream."
            % (node.Class(), node.Class())
        )
        return

    ## run the script - (NOTE: node must be passed here to avoid silent selection errors)
    settings = setup_breakout_panel(node)

    ## if the user clicked Cancel or closed the window, abort the script
    if not settings:
        return

    ## if the user selected 'Utilities' (meaning both mats and lights are False)
    if not settings['breakout_materials'] and not settings['breakout_lightgroups']:
        if settings['breakout_utilities']:
            breakout_utilities(node, settings)
        return  ## stop execution so no main pipe or cleanup is triggered

    if settings.get('rebuild_mode') == 'Additive':
        additive_breakout_lightgroups_and_materials(node, settings)
    elif settings.get('rebuild_mode') == 'Subtractive':
        subtractive_breakout_lightgroups_and_materials(node, settings)

    ## post-run warning: check for non read nodes
    if node.Class() != 'Read':
        nuke.message(
            "Warning: Selected node is a %s node.\n\n"
            "Please be careful of upstream operations such as Unpremult\n\n"
            "so not to break your AOV rebuild."
            % node.Class()
        )

    ## run the post pass after building
    if settings.get('rebuild_mode') == 'Additive':
        additive_post_layout_adjustments()
    elif settings.get('rebuild_mode') == 'Subtractive':
        subtractive_post_layout_adjustments(settings['x_space'], settings.get('x_dir', -1))


def breakout_utilities(node, settings=DEFAULT_SETTINGS):
    '''Cycles through all the aovs classed as utilities and creates an aov shuffle of them'''
    # print("running breakout_utilities") ## debug
    expected_utilities = settings['expected_utilities']
    x_space = settings['x_space']
    x_dir = settings.get('x_dir', -1)
    y_space = settings['y_space']

    utilities = get_utilities(node, expected_utilities)

    master_exclude = set(settings.get('omit_list', []) + settings.get('unassigned_list', []))
    utilities = [u for u in utilities if u not in master_exclude]

    ## Ensure alpha is ALWAYS present in the utility pipe
    if not any(u.lower() == 'alpha' for u in utilities):
        utilities.insert(0, 'alpha')

    if not utilities:
        return None

    bpipe_nodes = []
    x_pos, y_pos = get_centre_xypos(node)
    x_pos += (x_space * x_dir)

    utility_dot = nuke.nodes.Dot(inputs=[node])
    # utility_dot.setName('Utility_Pipe')
    utility_dot['label'].setValue('< UTILITY' + ' ' * 20)
    utility_dot["note_font_color"].setValue(int(0xFFFFFFFF))
    utility_dot["note_font"].setValue("bold")
    utility_dot["note_font_size"].setValue(40)
    set_centred_xypos(utility_dot, x_pos, y_pos)
    bpipe_nodes.append(utility_dot)

    x_utl_dot_pos, y_utl_dot_pos = get_centre_xypos(utility_dot)

    src_channels = set(node.channels())

    available_layers = get_all_layers(node)
    available_layers_lower = {l.lower() for l in available_layers}

    layout_index = 1

    ## initialize utility_rgba_node to prevent UnboundLocalError
    utility_rgba_node = None

    for utl in utilities:
        ## standard cases
        if utl.lower() != "other":
            x_pos = x_utl_dot_pos + (x_space * x_dir * layout_index)
            utility_pipe = [bpipe_nodes[-1]]

            utl_dot = nuke.nodes.Dot(inputs=[utility_pipe[-1]])
            set_centred_xypos(utl_dot, x_pos, y_pos)

            utility_pipe.append(utl_dot)
            bpipe_nodes.append(utl_dot)

            shuffle_utl = nuke.nodes.Shuffle2(inputs=[utility_pipe[-1]], in1=utl, in2='alpha', label=utl)

            ## alpha special-case (do not let generic mapping overwrite it)
            if utl.lower() == "alpha" and "alpha" not in available_layers_lower:
                shuffle_utl["in1"].setValue("rgba")
                shuffle_utl["in2"].setValue("rgba")
                shuffle_utl["label"].setValue("alpha")
                shuffle_utl["mappings"].setValue([
                    ("rgba.alpha", "rgba.red"),
                    ("rgba.alpha", "rgba.green"),
                    ("rgba.alpha", "rgba.blue"),
                    ("rgba.alpha", "rgba.alpha"),
                ])
            ## rgba special-case (do not let generic mapping overwrite it)
            elif utl.lower() == "rgba":
                shuffle_utl["in1"].setValue("rgba")
                shuffle_utl["in2"].setValue("rgba")
                shuffle_utl["label"].setValue("rgba")
                shuffle_utl["mappings"].setValue([
                    ("rgba.red", "rgba.red"),
                    ("rgba.green", "rgba.green"),
                    ("rgba.blue", "rgba.blue"),
                    ("rgba.alpha", "rgba.alpha"),
                ])
                shuffle_utl.setName('Utility_RGBA_Shuffle', True)
                utility_rgba_node = shuffle_utl
            else:
                ## gather channels that belong to this layer
                layer_chans = [c for c in src_channels if c.startswith(utl + ".")]

                has_xyz = all(f"{utl}.{c}" in src_channels for c in ("x", "y", "z"))
                has_rgb = all(f"{utl}.{c}" in src_channels for c in ("red", "green", "blue"))
                has_alpha = f"{utl}.alpha" in src_channels

                alpha_src = f"{utl}.alpha" if has_alpha else "rgba.alpha"

                if has_xyz:
                    try:
                        shuffle_utl['mappings'].setValue([
                            (f"{utl}.x", "rgba.red"),
                            (f"{utl}.y", "rgba.green"),
                            (f"{utl}.z", "rgba.blue"),
                            (alpha_src, "rgba.alpha"),
                        ])
                    except RuntimeError:
                        pass
                elif has_rgb:
                    try:
                        shuffle_utl['mappings'].setValue([
                            (f"{utl}.red", "rgba.red"),
                            (f"{utl}.green", "rgba.green"),
                            (f"{utl}.blue", "rgba.blue"),
                            (alpha_src, "rgba.alpha"),
                        ])
                    except RuntimeError:
                        pass
                else:
                    non_alpha = [c for c in layer_chans if not c.endswith(".alpha")]
                    single_src = (non_alpha[0] if non_alpha else (layer_chans[0] if layer_chans else None))

                    if single_src:
                        try:
                            shuffle_utl['mappings'].setValue([
                                (single_src, "rgba.red"),
                                (single_src, "rgba.green"),
                                (single_src, "rgba.blue"),
                                (alpha_src, "rgba.alpha"),
                            ])
                        except RuntimeError:
                            ## catch delayed evaluation of custom EXR channels and fallback
                            pass
                    else:
                        try:
                            shuffle_utl['mappings'].setValue([
                                (alpha_src, "rgba.alpha"),
                            ])
                        except RuntimeError:
                            pass

            shuffle_utl["note_font_color"].setValue(int(0xFFFFFFFF))
            shuffle_utl["note_font"].setValue("bold")
            set_centred_xypos(shuffle_utl, x_pos, y_pos + 28)
            utility_pipe.append(shuffle_utl)

            layout_index += 1

        ## special case: dynamic expansion for 'other' layer
        elif utl.lower() == "other":
            ## gather channels, skipping any stray alpha so it doesn't get its own node
            layer_chans = sorted([c for c in src_channels if c.startswith(utl + ".") and not c.endswith(".alpha")])
            has_alpha = f"{utl}.alpha" in src_channels
            alpha_src = f"{utl}.alpha" if has_alpha else "rgba.alpha"

            for chan in layer_chans:
                x_pos = x_utl_dot_pos + (x_space * x_dir * layout_index)
                utility_pipe = [bpipe_nodes[-1]]

                utl_dot = nuke.nodes.Dot(inputs=[utility_pipe[-1]])
                set_centred_xypos(utl_dot, x_pos, y_pos)

                utility_pipe.append(utl_dot)
                bpipe_nodes.append(utl_dot)

                ## extract the channel name and prefix it with 'other_' for the node label
                chan_name = chan.split('.')[-1]
                chan_label = f"other_{chan_name}"
                shuffle_utl = nuke.nodes.Shuffle2(inputs=[utility_pipe[-1]], in1=utl, in2='alpha', label=chan_label)

                try:
                    ## map the single channel to RGB for greyscale viewing
                    shuffle_utl['mappings'].setValue([
                        (chan, "rgba.red"),
                        (chan, "rgba.green"),
                        (chan, "rgba.blue"),
                        (alpha_src, "rgba.alpha"),
                    ])
                except RuntimeError:
                    pass

                shuffle_utl["note_font_color"].setValue(int(0xFFFFFFFF))
                shuffle_utl["note_font"].setValue("bold")
                set_centred_xypos(shuffle_utl, x_pos, y_pos + 28)
                utility_pipe.append(shuffle_utl)

                layout_index += 1

    return utility_dot, utility_rgba_node

def additive_lightgroups_or_materials(node, mode = 0, settings = DEFAULT_SETTINGS, start_input=None):
    '''Cycles through all the aovs classed as either materials (mode 0) or lightgroups (mode 1) and creates and aov minibuild of them'''
    ## breakout settings
    expected_materials = settings['expected_materials']
    lightgroup_regex = settings['lg_regex']
    additional_lighting = settings['additional_lighting']
    x_space = settings['x_space']
    x_dir = settings.get('x_dir', -1)
    y_space = settings['y_space']

    if start_input is None:
        start_input = node

    bpipe_nodes = []
    x_pos, y_pos = get_centre_xypos(node)

    no_op = nuke.nodes.NoOp(inputs = [start_input])
    no_op.setName('spacer_no_op', True)
    set_centred_xypos(no_op, x_pos, y_pos)
    bpipe_nodes.append(no_op)

    x_pos += (x_space * x_dir)
    start_dot = nuke.nodes.Dot(inputs = [bpipe_nodes[-1]])
    start_dot.setName('start_dot', True)
    #start_dot['label'].setValue('start_dot') ## debug layout
    set_centred_xypos(start_dot, x_pos, y_pos)
    bpipe_nodes.append(start_dot)
    entry_nodes =[bpipe_nodes[-1]]
    ## ensure bpipe_xpos/ypos always exist even if no AOVs are found
    bpipe_xpos, bpipe_ypos = get_centre_xypos(bpipe_nodes[-1])

    ## main breakout
    if mode == 0:
        lightgroups_or_materials = get_materials(node, expected_materials)
    elif mode == 1:
        ## use the user-curated list when available, otherwise fall back to regex
        if settings.get('custom_lightgroups') is not None:
            lightgroups_or_materials = settings['custom_lightgroups']
        else:
            lightgroups_or_materials = get_lightgroup_layers(
                node, lightgroup_regex, additional_lighting,
                exclude=settings.get('lg_exclude', []) ## deduplicate against materials
            )

    master_exclude = set(settings.get('omit_list', []) + settings.get('unassigned_list', []))
    lightgroups_or_materials = [item for item in lightgroups_or_materials if item not in master_exclude]

    ## feedback to artist on missing material AOVs
    # if not lightgroups_or_materials:
    #     sticky_label = '<h3>Missing Materials</h3>There are no materials in this stream.'
    #     sticky_note = nuke.nodes.StickyNote(
    #         label=sticky_label,
    #         tile_color=0x272727ff,
    #         note_font_color=0xa8a8a8ff,
    #         note_font_size=40
    #     )
    #     sticky_note.setXYpos(int(x_pos + (x_space * x_dir) * 3), int(y_pos))
    #     return bpipe_nodes

    count = 0 ## track Lightgroup numbers

    for lg in lightgroups_or_materials:
        x_pos, y_pos = get_centre_xypos(entry_nodes[-1])
        x_pos += (x_space * x_dir)

        ## aov_pipe
        aov_pipe = []
        aov_dot = nuke.nodes.Dot(inputs = [entry_nodes[-1]])
        aov_dot.setName('aov_dot', True)
        #aov_dot['label'].setValue('aov_dot') ## debug layout
        set_centred_xypos(aov_dot, x_pos, y_pos)
        entry_nodes.append(aov_dot)
        aov_pipe.append(aov_dot)

        y_pos+=y_space
        shuffle_aov = nuke.nodes.Shuffle2(inputs = [aov_pipe[-1]], in1 = lg, in2 = 'alpha', label = lg)
        shuffle_aov['mappings'].setValue([('rgba.alpha','rgba.alpha')])
        shuffle_aov["note_font_color"].setValue(int(0xFFFFFFFF))
        shuffle_aov["note_font"].setValue("bold")
        set_centred_xypos(shuffle_aov, x_pos, y_pos)
        aov_pipe.append(shuffle_aov)

        y_pos+=y_space
        bottom_aov_dot = nuke.nodes.Dot(inputs = [aov_pipe[-1]])
        bottom_aov_dot.setName('bottom_aov_dot', True)
        #bottom_aov_dot['label'].setValue('bottom_aov_dot')  ## debug layout
        set_centred_xypos(bottom_aov_dot, x_pos, y_pos)
        aov_pipe.append(bottom_aov_dot)

        ## bpipe
        lg_lower = lg.lower()
        skip_bpipe = False

        if mode == 0:
            ## build a clean lookup, stripping all outer underscores to immune the check against prefixes / suffixes
            all_mats_clean = [m.lower().strip('_') for m in lightgroups_or_materials]
            lg_clean = lg_lower.strip('_')

            base_suffix = None
            if 'combined' in lg_clean:
                ## remove 'combined' and strip any dangling underscores
                base_suffix = lg_clean.replace('combined', '').strip('_')
            elif lg_clean in ('diffuse', 'specular', 'sss', 'reflection', 'coat', 'sheen', 'transmission', 'emission', 'volume'):
                base_suffix = lg_clean

            if base_suffix:
                ## generate possible direct/indirect naming syntax variations (0, 1, or 2 underscores)
                direct_vars = [f"direct{sep}{base_suffix}" for sep in ("", "_", "__")] + \
                              [f"{base_suffix}{sep}direct" for sep in ("", "_", "__")]

                indirect_vars = [f"indirect{sep}{base_suffix}" for sep in ("", "_", "__")] + \
                                [f"{base_suffix}{sep}indirect" for sep in ("", "_", "__")]

                has_direct = any(d in all_mats_clean for d in direct_vars)
                has_indirect = any(i in all_mats_clean for i in indirect_vars)

                if has_direct and has_indirect:
                    sticky_label = (
                            "%s not added to B pipe,\n\n"
                            "direct and indirect layers used."
                            % (lg)
                    )
                    sticky_note = nuke.nodes.StickyNote(
                        label=sticky_label,
                        tile_color=0x272727ff,
                        note_font_color=0xa8a8a8ff,
                        note_font_size=11,
                    )
                    target_x, target_y = get_centre_xypos(shuffle_aov)
                    set_centred_xypos(sticky_note, x_pos, target_y - 25)
                    continue

        ## universal guards (apply to both materials and lightgroups)
        if lg_lower in ("ao", "gi") or "raw" in lg_lower or "filter" in lg_lower or "shadow" in lg_lower:
            sticky_label = (
                    "%s not added to B pipe,\n\n"
                    "This AOV will break the basic rebuild.\n\n"
                    "Please use as needed"
            ) % (lg)
            sticky_note = nuke.nodes.StickyNote(
                label=sticky_label,
                tile_color=0x272727ff,
                note_font_color=0xa8a8a8ff,
                note_font_size=11,
            )
            target_x, target_y = get_centre_xypos(shuffle_aov)
            set_centred_xypos(sticky_note, x_pos, target_y - 25)
            skip_bpipe = True

        ## skip albedo AOVs in B pipe (materials rebuild only)
        if mode == 0 and ('albedo' in lg_lower or 'color' in lg_lower or 'colour' in lg_lower or lg_lower == 'c'):

            ## ensure the RGB remove happens once at the start of the bpipe
            bpipe_xpos, bpipe_ypos = get_centre_xypos(bpipe_nodes[-1])

            if count == 0:
                remove_rgb = nuke.nodes.Remove(
                    operation='remove',
                    channels='rgb',
                    inputs=[bpipe_nodes[-1]],
                    label='RGB',
                    note_font_color=0xFFFFFFFF,
                    note_font='bold'
                )
                set_centred_xypos(remove_rgb, bpipe_xpos, bpipe_ypos + y_space)
                bpipe_nodes.append(remove_rgb)

                ## mark "first" as handled so we don't create remove_rgb again next iteration
                count = 1

                ## update bpipe position now that remove_rgb is appended
                bpipe_xpos, bpipe_ypos = get_centre_xypos(bpipe_nodes[-1])

            ## reserve the same vertical space a merge_plus would take (keeps layout unchanged)
            merge_ypos = bpipe_ypos + (y_space * 3)

            albedo_spacer_dot = nuke.nodes.Dot(inputs=[bpipe_nodes[-1]])
            albedo_spacer_dot.setName('albedo_spacer_dot', True)
            #albedo_spacer_dot['label'].setValue('albedo_skipped')  ## debug layout
            set_centred_xypos(albedo_spacer_dot, bpipe_xpos, merge_ypos)
            bpipe_nodes.append(albedo_spacer_dot)

            ## keep the aov branch bottom aligned to the bpipe row
            y_pos = merge_ypos
            set_centred_xypos(aov_pipe[-1], x_pos, y_pos)

            sticky_label = (
                "%s not added to B pipe,\n\n"
                "This AOV will break the basic rebuild.\n\n"
                "Please use as needed"
            ) % (lg)
            sticky_note = nuke.nodes.StickyNote(
                label=sticky_label,
                tile_color=0x272727ff,
                note_font_color=0xa8a8a8ff,
                note_font_size=11,
            )
            target_x, target_y = get_centre_xypos(shuffle_aov)
            set_centred_xypos(sticky_note, x_pos, target_y - 25)

        elif skip_bpipe:
            ## skipped AOVs: do nothing further to bpipe (no spacer dots, no remove node, no merge)
            pass
        else:
            bpipe_xpos, bpipe_ypos = get_centre_xypos(bpipe_nodes[-1])

            if count==0:
                remove_rgb = nuke.nodes.Remove(
                    operation='remove',
                    channels='rgb',
                    inputs=[bpipe_nodes[-1]],
                    label='RGB',
                    note_font_color=0xFFFFFFFF,
                    note_font='bold'
                )
                set_centred_xypos(remove_rgb, bpipe_xpos, bpipe_ypos+y_space)
                bpipe_nodes.append(remove_rgb)

            bpipe_ypos += y_space * 2

            bpipe_ypos += y_space
            merge_plus = nuke.nodes.Merge2(
                inputs=[bpipe_nodes[-1], aov_pipe[-1]],
                operation='plus',
                output='rgb',
                tile_color=MERGE_PLUS_COLOUR,
                label=lg
            )
            set_centred_xypos(merge_plus, bpipe_xpos, bpipe_ypos)
            bpipe_nodes.append(merge_plus)

            y_pos = bpipe_ypos
            set_centred_xypos(aov_pipe[-1], x_pos, y_pos)

            count += 1

    ## unassigned pipe
    unassigned_pipe = []
    x_pos += (x_space * x_dir)
    unassigned_aov_dot = nuke.nodes.Dot(inputs = [entry_nodes[-1]])
    #unassigned_aov_dot['label'].setValue('unassigned_aov_dot') ## debug layout
    unassigned_ypos = get_centre_xypos(entry_nodes[-1], )[1]
    set_centred_xypos(unassigned_aov_dot, x_pos, unassigned_ypos)
    entry_nodes.append(unassigned_aov_dot)
    unassigned_pipe.append(unassigned_aov_dot)

    unassigned_ypos += y_space
    shuffle_original = nuke.nodes.Shuffle2(inputs = [unassigned_pipe[-1]], in1 = 'original', label = 'original rgb', note_font_color = 0xFFFFFFFF, note_font = 'bold')
    set_centred_xypos(shuffle_original, x_pos, unassigned_ypos)
    unassigned_pipe.append(shuffle_original)

    for lg in lightgroups_or_materials:
        unassigned_ypos += y_space
        bpipe_ypos += y_space * 0.5
        merge_from = nuke.nodes.Merge2(inputs = [unassigned_pipe[-1], unassigned_pipe[-1]], Achannels = lg, operation ='from', output = 'rgb', tile_color = MERGE_FROM_COLOUR, label = lg)
        set_centred_xypos(merge_from, x_pos, unassigned_ypos)
        unassigned_pipe.append(merge_from)

        y_pos += y_space * 0.5

    ## qc check
    run_qc = False
    ct = None  ## initialize so it exists even if QC is skipped
    if mode == 0 and settings.get('check_unassigned_values_mats'):
        run_qc = True
        qc_name = "Check_Values_Materials\n\nMin Luma Pix Value: [value minlumapixvalue]"
    elif mode == 1 and settings.get('check_unassigned_values_lights'):
        run_qc = True
        qc_name = "Check_Values_Lightgroups\n\nMin Luma Pix Value: [value minlumapixvalue]"

    if run_qc:
        ct = nuke.nodes.CurveTool(inputs=[unassigned_pipe[-1]], note_font_color = 0xFFFFFFFF, note_font = 'bold')
        #ct.setName(qc_name, True) ## debug
        ct['label'].setValue(qc_name)
        ct['operation'].setValue('Max Luma Pixel')

        w, h = ct.input(0).width(), ct.input(0).height()
        ct['ROI'].setValue([0, 0, w, h])
        ct['ROI'].clearAnimated()

        unassigned_ypos += y_space
        set_centred_xypos(ct, x_pos, unassigned_ypos)

        nuke.execute(ct, int(nuke.root()['first_frame'].value()), int(nuke.root()['last_frame'].value()))
        unassigned_pipe.append(ct)

    unassigned_bottom_dot = nuke.nodes.Dot(inputs=[unassigned_pipe[-1]])
    unassigned_bottom_dot.setName('unassigned_bottom_dot', True)
    #unassigned_bottom_dot['label'].setValue('unassigned_bottom_dot') ## debug layout
    set_centred_xypos(unassigned_bottom_dot, x_pos, bpipe_ypos)

    if run_qc and ct:
        analysis_results = ct['minlumapixvalue'].value()
        has_negatives = any(v < 0 for v in analysis_results)

        if has_negatives:
            ## red / disconnect
            ct['tile_color'].setValue(MERGE_FROM_COLOUR)
            unassigned_bottom_dot.setInput(0, None)  ## disconnect unassigned_bottom_dot
            msg = "<font color=#eb4c34><b>Negative Values</b></font>\nUnassigned pipe disconnected. Negative values should not be plussed to the B pipe"
            sn = nuke.nodes.StickyNote(label=msg, tile_color=0x272727ff, note_font_color=0xa8a8a8ff, note_font_size=20)
            sn.setXYpos(int(x_pos + (x_space * x_dir) * 3.2), unassigned_ypos - 28)
        else:
            ## green / stay connected
            ct['tile_color'].setValue(MERGE_PLUS_COLOUR)
            msg = "<font color=#70EE70><b>Positive Values</b></font>\nUnassigned pipe may be plussed to the B pipe."
            sn = nuke.nodes.StickyNote(label=msg, tile_color=0x272727ff, note_font_color=0xa8a8a8ff, note_font_size=20)
            sn.setXYpos(int(x_pos + (x_space * x_dir) * 2.1), unassigned_ypos - 28)

    ## append the dot to the final list for the return
    unassigned_pipe.append(unassigned_bottom_dot)

    merge_plus = nuke.nodes.Merge2(inputs = [bpipe_nodes[-1], unassigned_pipe[-1]], operation ='plus', output = 'rgb', tile_color = MERGE_PLUS_COLOUR, label = '<i> unassigned aovs', disable = True)
    merge_plus.setName('merge_plus', True)
    set_centred_xypos(merge_plus, bpipe_xpos, bpipe_ypos)
    bpipe_nodes.append(merge_plus)

    bpipe_ypos += y_space
    end_result = nuke.nodes.Dot(inputs =[bpipe_nodes[-1]])
    end_result.setName('end_result', True)
    #end_result['label'].setValue('end_result')  ## debug layout
    set_centred_xypos(end_result, bpipe_xpos, bpipe_ypos)
    bpipe_nodes.append(end_result)

    return bpipe_nodes

def additive_breakout_lightgroups_and_materials(node, settings=DEFAULT_SETTINGS):
    '''Runs an additive breakout of materials and lightgroups using divide/multiply to combine both operations in a mathematically correct fashion.'''
    breakout_utilities_enabled = settings.get('breakout_utilities', False)

    ## breakout settings
    breakout_materials = settings['breakout_materials']
    breakout_lightgroups = settings['breakout_lightgroups']
    expected_materials = settings['expected_materials']
    expected_utilities = settings['expected_utilities']
    lightgroup_regex = settings['lg_regex']
    additional_lighting = settings['additional_lighting']
    x_space = settings['x_space']
    x_dir = settings.get('x_dir', -1)
    y_space = settings['y_space']

    ## if there are no materials/lightgroups, run utilities only (if any)
    materials  = get_materials(node, expected_materials)
    ## respect user-edited list; otherwise exclude anything already classed as a material
    if settings.get('custom_lightgroups') is not None:
        lightgroups = settings['custom_lightgroups']
    else:
        lightgroups = get_lightgroup_layers(
            node, lightgroup_regex, additional_lighting,
            exclude=settings.get('lg_exclude', [])
        )
    utilities  = get_utilities(node, expected_utilities)
    utility_dot = None
    utility_rgba_node = None

    master_exclude = set(settings.get('omit_list', []) + settings.get('unassigned_list', []))
    materials = [m for m in materials if m not in master_exclude]
    lightgroups = [lg for lg in lightgroups if lg not in master_exclude]
    utilities = [u for u in utilities if u not in master_exclude]

    if breakout_utilities_enabled:
        utl_result = breakout_utilities(node, settings)
        if utl_result:
            utility_dot, utility_rgba_node = utl_result

    ## guard : utilities only mode / fallback
    if not materials and not lightgroups:
        return

    ## begin main bpipe
    bpipe_nodes = []
    x_pos, y_pos = get_centre_xypos(node)
    y_pos += y_space

    ## identify which utilities are in the stream
    utilities_to_remove = get_utilities(node, settings['expected_utilities'])

    ## filter out 'rgba' and 'alpha' so they are not removed
    filtered_utilities = [utl for utl in utilities_to_remove if utl not in ('rgba', 'alpha')]

    if filtered_utilities:
        ## do not connect inputs yet
        remove_utilities_grp = nuke.nodes.Group() ## (label='Remove Utilities')
        remove_utilities_grp.setName('Remove_Utilities', True)
        remove_utilities_grp["tile_color"].setValue(int(0x9e3c6300))
        remove_utilities_grp["note_font_color"].setValue(int(0xFFFFFFFF))
        remove_utilities_grp["note_font"].setValue("bold")
        set_centred_xypos(remove_utilities_grp, x_pos, y_pos)

        ## create and add the Tab_Knob
        user_tab = nuke.Tab_Knob('removed_list_tab', 'Removed List')
        remove_utilities_grp.addKnob(user_tab)

        ## format the list of removed utilities (joined by line breaks for a clean list)
        removed_layers_str = '\n'.join(filtered_utilities)

        ## create a Text_Knob to display the string (ideal for read-only information)
        removed_info_knob = nuke.Text_Knob('removed_layers_info', '', removed_layers_str)
        remove_utilities_grp.addKnob(removed_info_knob)

        with remove_utilities_grp:
            grp_input = nuke.nodes.Input()
            curr_node = grp_input
            ## create one remove node for each utility layer
            for utl in filtered_utilities:  ## use the filtered list here
                remove_node = nuke.nodes.Remove(inputs=[curr_node], operation='remove', channels=utl)
                remove_node["note_font_color"].setValue(int(0xFFFFFFFF))
                remove_node["note_font"].setValue("bold")

                curr_node = remove_node
            ## cap off the inside of the group
            nuke.nodes.Output(inputs=[curr_node])
        ## connect the external pipe
        remove_utilities_grp.setInput(0, node)
    else:
        ## fallback to standard NoOp if no utilities exist (or if only rgba/alpha were present)
        remove_utilities_grp = nuke.nodes.NoOp(inputs=[node])
        remove_utilities_grp.setName('spacer_no_op', True)
        set_centred_xypos(remove_utilities_grp, x_pos, y_pos)

    bpipe_nodes.append(remove_utilities_grp)
    y_pos += y_space

    ## get all layers in the stream to check for crypto
    all_stream_layers = get_all_layers(node)

    ## filter for any layers containing 'crypto' (case-insensitive)
    crypto_layers = [layer for layer in all_stream_layers if 'crypto' in layer.lower()]

    if crypto_layers:
        ## create a group to house the remove nodes cleanly
        remove_crypto_grp = nuke.nodes.Group()
        remove_crypto_grp.setName('Remove_Crypto', True)
        remove_crypto_grp["tile_color"].setValue(int(0x9e3c6300))
        remove_crypto_grp["note_font_color"].setValue(int(0xFFFFFFFF))
        remove_crypto_grp["note_font"].setValue("bold")
        set_centred_xypos(remove_crypto_grp, x_pos, y_pos)

        ## create and add the Tab_Knob
        crypto_tab = nuke.Tab_Knob('crypto_list_tab', 'Crypto List')
        remove_crypto_grp.addKnob(crypto_tab)

        ## format the list of removed crypto layers (joined by line breaks)
        crypto_layers_str = '\n'.join(crypto_layers)

        ## create a Text_Knob to display the string
        crypto_info_knob = nuke.Text_Knob('crypto_layers_info', '', crypto_layers_str)
        remove_crypto_grp.addKnob(crypto_info_knob)

        with remove_crypto_grp:
            grp_input = nuke.nodes.Input()
            curr_node = grp_input

            ## create one remove node for each crypto layer
            for c_layer in crypto_layers:
                remove_node = nuke.nodes.Remove(inputs=[curr_node], operation='remove', channels=c_layer)
                remove_node["note_font_color"].setValue(int(0xFFFFFFFF))
                remove_node["note_font"].setValue("bold")

                curr_node = remove_node

            ## cap off the inside of the group
            nuke.nodes.Output(inputs=[curr_node])

        ## connect the external pipe to the last node in the bpipe
        remove_crypto_grp.setInput(0, bpipe_nodes[-1])
        bpipe_nodes.append(remove_crypto_grp)
        y_pos += y_space

    unpremult_aov = nuke.nodes.Unpremult(inputs=[bpipe_nodes[-1]], )
    #unpremult_original['channels'].setValue('original')
    unpremult_aov['channels'].setValue('all')
    set_centred_xypos(unpremult_aov, x_pos, y_pos)
    bpipe_nodes.append(unpremult_aov)
    y_pos += y_space

    ## initialize a tracking variable for the compare switch
    last_merge_materials = None
    ## index to dynamically assign 01 or 02 to the built pipes
    breakout_index = 1

    ## materials breakout
    if breakout_materials == True and materials:
        b_pipe_top_dot = nuke.nodes.Dot(inputs=[bpipe_nodes[-1]], )
        b_pipe_top_dot.setName('b_pipe_top_0%s_dot' % breakout_index, True)
        #b_pipe_top_dot['label'].setValue('b_pipe_top_0%s_dot' % breakout_index)  ## debug layout
        set_centred_xypos(b_pipe_top_dot, x_pos, y_pos)
        bpipe_nodes.append(b_pipe_top_dot)

        if breakout_index == 1:
            beauty_dot = nuke.nodes.Dot(inputs=[b_pipe_top_dot])
            beauty_dot.setName('beauty_dot', True)
            #beauty_dot['label'].setValue('beauty_dot')  ## debug layout
            set_centred_xypos(beauty_dot, x_pos - (x_space * x_dir), y_pos)

        x_pos += (x_space * x_dir)

        mat_pipe = additive_lightgroups_or_materials(b_pipe_top_dot, 0, settings)
        x_pos = get_centre_xypos(bpipe_nodes[-1])[0]
        y_pos = get_centre_xypos(mat_pipe[-1])[1]

        b_pipe_btm_dot = nuke.nodes.Dot(inputs=[bpipe_nodes[-1]])
        b_pipe_btm_dot.setName('b_pipe_btm_0%s_dot' % breakout_index, True)
        #b_pipe_btm_dot['label'].setValue('b_pipe_btm_0%s_dot' % breakout_index)  ## debug layout
        set_centred_xypos(b_pipe_btm_dot, x_pos, y_pos)
        bpipe_nodes.append(b_pipe_btm_dot)

        y_pos += y_space
        merge_divide = nuke.nodes.Merge2(inputs=[bpipe_nodes[-1], mat_pipe[-1]], operation='divide', output='rgb')
        set_centred_xypos(merge_divide, get_centre_xypos(mat_pipe[-1])[0], y_pos)
        mat_pipe.append(merge_divide)

        y_pos += y_space
        merge_materials = nuke.nodes.Merge2(inputs=[bpipe_nodes[-1], mat_pipe[-1]], operation='multiply', output='rgb')
        set_centred_xypos(merge_materials, x_pos, y_pos)
        bpipe_nodes.append(merge_materials)

        last_merge_materials = merge_materials

        breakout_index += 1

        y_pos += y_space

    ## lightgroups breakout
    if breakout_lightgroups == True and lightgroups:
        b_pipe_top_dot = nuke.nodes.Dot(inputs=[bpipe_nodes[-1]], )
        b_pipe_top_dot.setName('b_pipe_top_0%s_dot' % breakout_index, True)
        #b_pipe_top_dot['label'].setValue('b_pipe_top_0%s_dot' % breakout_index)  ## debug layout
        set_centred_xypos(b_pipe_top_dot, x_pos, y_pos)
        bpipe_nodes.append(b_pipe_top_dot)

        if breakout_index == 1:
            beauty_dot = nuke.nodes.Dot(inputs=[b_pipe_top_dot])
            beauty_dot.setName('beauty_dot', True)
            #beauty_dot['label'].setValue('beauty_dot')  ## debug layout
            set_centred_xypos(beauty_dot, x_pos - (x_space * x_dir), y_pos)

        x_pos += (x_space * x_dir)

        lg_pipe = additive_lightgroups_or_materials(b_pipe_top_dot, 1, settings)
        x_pos = get_centre_xypos(bpipe_nodes[-1])[0]
        y_pos = get_centre_xypos(lg_pipe[-1])[1]

        b_pipe_btm_dot = nuke.nodes.Dot(inputs=[bpipe_nodes[-1]])
        b_pipe_btm_dot.setName('b_pipe_btm_0%s_dot' % breakout_index, True)
        #b_pipe_btm_dot['label'].setValue('b_pipe_btm_0%s_dot' % breakout_index)  ## debug layout
        set_centred_xypos(b_pipe_btm_dot, x_pos, y_pos)
        bpipe_nodes.append(b_pipe_btm_dot)

        y_pos += y_space
        merge_divide = nuke.nodes.Merge2(inputs=[bpipe_nodes[-1], lg_pipe[-1]], operation='divide', output='rgb')
        set_centred_xypos(merge_divide, get_centre_xypos(lg_pipe[-1])[0], y_pos)
        lg_pipe.append(merge_divide)

        y_pos += y_space
        merge_materials = nuke.nodes.Merge2(inputs=[bpipe_nodes[-1], lg_pipe[-1]], operation='multiply', output='rgb')
        set_centred_xypos(merge_materials, x_pos, y_pos)
        bpipe_nodes.append(merge_materials)

        last_merge_materials = merge_materials

        breakout_index += 1

    ## build compare switch
    if last_merge_materials:
        y_pos += y_space

        ## get the x pos of the last shuffle to align the vertical line
        switch_dot_x, _ = get_centre_xypos(beauty_dot)

        switch_dot = nuke.nodes.Dot(inputs=[beauty_dot])
        switch_dot.setName('switch_dot', True)
        # switch_dot['label'].setValue('switch_dot') ## debug layout
        set_centred_xypos(switch_dot, switch_dot_x, y_pos)

        compare_switch = nuke.nodes.Switch(inputs=[bpipe_nodes[-1], switch_dot], label='Compare Beauty')
        compare_switch["note_font_color"].setValue(int(0xFFFFFFFF))
        compare_switch["note_font"].setValue("bold")
        set_centred_xypos(compare_switch, x_pos, y_pos)
        bpipe_nodes.append(compare_switch)

        y_pos += y_space

        ## create a Dot for the Copy node
        copy_dot = nuke.nodes.Dot(inputs=[switch_dot])
        copy_dot.setName('copy_dot', True)
        # copy_dot['label'].setValue('copy_dot') ## debug layout
        set_centred_xypos(copy_dot, switch_dot_x, y_pos)

        ## copy the original alpha back into the rebuilt stream
        copy_alpha = nuke.nodes.Copy(inputs=[bpipe_nodes[-1], copy_dot], from0='rgba.alpha', to0='rgba.alpha')
        set_centred_xypos(copy_alpha, x_pos, y_pos)
        bpipe_nodes.append(copy_alpha)

    final_premult = nuke.nodes.Premult(inputs=[bpipe_nodes[-1]])
    set_centred_xypos(final_premult, x_pos, y_pos + 32)
    bpipe_nodes.append(final_premult)

    keep_rgba = nuke.nodes.Remove(inputs=[bpipe_nodes[-1]], operation='keep', channels='rgba')
    set_centred_xypos(keep_rgba, x_pos, y_pos + 58)
    bpipe_nodes.append(keep_rgba)

def additive_post_layout_adjustments(y_offset_shuffle=28, y_offset_unpremult=32, y_pad_bottom_dot=50):
    '''Runs a layout adjustment for various nodes and deletes placeholder nodes not relevant to the network.'''
    deleted_NoOps = 0
    ## move Shuffle2 nodes up to the minimum Y of their upstream aov_dot + offset
    for sh in nuke.allNodes():
        if (
            sh.Class() == 'Shuffle2'
            or (sh.Class() == 'Remove' and sh['label'].value() == 'RGB')
        ):
            inp = sh.input(0)
            if not inp:
                continue

            if inp.Class() == 'Dot' and ('aov_dot' in inp.name() or 'start_dot' in inp.name()):
                sh_x, _ = get_centre_xypos(sh)
                _, dot_y = get_centre_xypos(inp)

                target_y = int(dot_y + y_offset_shuffle)
                set_centred_xypos(sh, sh_x, target_y)

    ## bottom_aov_dot: align to upstream node, then place below using upstream size
    for d in nuke.allNodes('Dot'):
        if "bottom_aov_dot" in d.name().lower() and len(d.dependent(nuke.INPUTS)) == 0:

            up = d.input(0)
            if not up:
                continue

            up_x, up_y = get_centre_xypos(up)
            # half upstream height + half dot height + padding
            offset = int((up.screenHeight() / 2) + (d.screenHeight() / 2) + y_pad_bottom_dot)
            set_centred_xypos(d, up_x, int(up_y + offset))

    ## delete albedo_spacer_dot
    for n in nuke.allNodes('Dot'):
        if 'albedo_spacer_dot' in n.name():
            nuke.delete(n)

    merge_pluses = [
        n for n in nuke.allNodes("Merge2")
        if n.name().startswith("merge_plus")
    ]
    unassigned_bottom_dot = nuke.toNode("unassigned_bottom_dot")

    if unassigned_bottom_dot:
        for m in merge_pluses:
            if unassigned_bottom_dot in m.dependencies():
                ux, _ = get_centre_xypos(unassigned_bottom_dot)
                _, my = get_centre_xypos(m)
                set_centred_xypos(unassigned_bottom_dot, ux, my)
                break

    ## delete end_result (dot)
    for n in nuke.allNodes('Dot'):
        if 'end_result' in n.name():
            nuke.delete(n)

    ## delete NoOps
    for n in nuke.allNodes('NoOp'):
        if 'spacer_no_op' in n.name():
            nuke.delete(n)
            deleted_NoOps += 1

    print("post_layout_adjustments() ran:",
          "deleted_NoOps =", deleted_NoOps)

def subtractive_lightgroups_or_materials(node, mode = 0, settings = DEFAULT_SETTINGS, start_input=None, upstream_aov_dot=None, upstream_unassigned_dot=None):
    '''Cycles through all the aovs classed as either materials (mode 0) or lightgroups (mode 1) and creates and aov minibuild of them'''
    ## breakout settings
    expected_materials = settings['expected_materials']
    lightgroup_regex = settings['lg_regex']
    additional_lighting = settings['additional_lighting']
    x_space = settings['x_space']
    x_dir = settings.get('x_dir', -1)
    y_space = settings['y_space']

    if start_input is None:
        start_input = node

    ## define a name suffix based on whether this is a material or lightgroup pipe
    pipe_suffix = "_lg" if mode == 1 else "_mat"

    bpipe_nodes = []
    x_pos, y_pos = get_centre_xypos(node)

    x_pos += (x_space * x_dir) ## * 0.5
    start_dot = nuke.nodes.Dot(inputs=[start_input])
    ## apply suffix to the name.
    start_dot.setName('start_dot' + pipe_suffix, True)
    #start_dot['label'].setValue('start_dot' + pipe_suffix) ## debug layout
    set_centred_xypos(start_dot, x_pos, y_pos)
    bpipe_nodes.append(start_dot)

    x_pos += (x_space * x_dir)
    if upstream_aov_dot:
        start_aov_dot = nuke.nodes.Dot(inputs=[upstream_aov_dot])
    else:
        start_aov_dot = nuke.nodes.Dot(inputs=[bpipe_nodes[-1]])

    start_aov_dot.setName('start_aov_dot' + pipe_suffix, True)
    #start_aov_dot['label'].setValue('start_aov_dot' + pipe_suffix) ## debug layout

    if mode == 1 and upstream_aov_dot is not None:
        y_pos += y_space

    set_centred_xypos(start_aov_dot, x_pos, y_pos)
    bpipe_nodes.append(start_aov_dot)

    entry_nodes = [start_aov_dot]
    bpipe_xpos, bpipe_ypos = get_centre_xypos(start_dot)

    ## main breakout
    if mode == 0:
        lightgroups_or_materials = get_materials(node, expected_materials)
    elif mode == 1:
        ## use the user-curated list when available, otherwise fall back to regex
        if settings.get('custom_lightgroups') is not None:
            lightgroups_or_materials = settings['custom_lightgroups']
        else:
            lightgroups_or_materials = get_lightgroup_layers(
                node, lightgroup_regex, additional_lighting,
                exclude=settings.get('lg_exclude', [])   ## deduplicate against materials
            )

    master_exclude = set(settings.get('omit_list', []) + settings.get('unassigned_list', []))
    lightgroups_or_materials = [item for item in lightgroups_or_materials if item not in master_exclude]

    ## feedback to artist on missing material AOVs
    # if not lightgroups_or_materials:
    #     sticky_label = '<h3>Missing Materials</h3>There are no materials in this stream.'
    #     sticky_note = nuke.nodes.StickyNote(
    #         label=sticky_label,
    #         tile_color=0x272727ff,
    #         note_font_color=0xa8a8a8ff,
    #         note_font_size=40
    #     )
    #     sticky_note.setXYpos(int(x_pos - (x_space * x_dir) * 7), int(y_pos))
    #     return bpipe_nodes, start_aov_dot, None

    count = 0 ## track Lightgroup numbers

    ## track which AOVs were successfully added to the B-pipe
    valid_aovs_for_unassigned = []
    first_merge = True

    for i, lg in enumerate(lightgroups_or_materials):
        x_pos, y_pos = get_centre_xypos(entry_nodes[-1])

        ## apply a different offset for the first iteration
        if i == 0:
            y_pos += y_space * 2
        else:
            y_pos += y_space * 4

        ## aov_pipe
        aov_pipe = []
        aov_dot = nuke.nodes.Dot(inputs=[entry_nodes[-1]])
        #aov_dot.setName('aov_dot', True) ## debug
        #aov_dot['label'].setValue('aov_dot')  ## debug layout
        set_centred_xypos(aov_dot, x_pos, y_pos)
        entry_nodes.append(aov_dot)
        aov_pipe.append(aov_dot)

        x_pos -= (x_space * x_dir) * 0.5
        shuffle_aov = nuke.nodes.Shuffle2(inputs=[aov_pipe[-1]], in1=lg, in2='alpha', label=lg)
        shuffle_aov['mappings'].setValue([('rgba.alpha', 'rgba.alpha')])
        shuffle_aov["note_font_color"].setValue(int(0xFFFFFFFF))
        shuffle_aov["note_font"].setValue("bold")
        set_centred_xypos(shuffle_aov, int(x_pos), y_pos)
        aov_pipe.append(shuffle_aov)

        ## guards to skip problematic AOVs
        skip_bpipe = False
        lg_lower = lg.lower()

        if mode == 0:
            ## build a clean lookup, stripping all outer underscores to immune the check against prefixes / suffixes
            all_mats_clean = [m.lower().strip('_') for m in lightgroups_or_materials]
            lg_clean = lg_lower.strip('_')

            base_suffix = None
            if 'combined' in lg_clean:
                ## remove 'combined' and strip any dangling underscores
                base_suffix = lg_clean.replace('combined', '').strip('_')
            elif lg_clean in ('diffuse', 'specular', 'sss', 'reflection', 'coat', 'sheen', 'transmission', 'emission', 'volume'):
                base_suffix = lg_clean

            if base_suffix:
                ## generate possible direct/indirect naming syntax variations (0, 1, or 2 underscores)
                direct_vars = [f"direct{sep}{base_suffix}" for sep in ("", "_", "__")] + \
                              [f"{base_suffix}{sep}direct" for sep in ("", "_", "__")]

                indirect_vars = [f"indirect{sep}{base_suffix}" for sep in ("", "_", "__")] + \
                                [f"{base_suffix}{sep}indirect" for sep in ("", "_", "__")]

                has_direct = any(d in all_mats_clean for d in direct_vars)
                has_indirect = any(i in all_mats_clean for i in indirect_vars)

                if has_direct and has_indirect:
                    sticky_label = (
                            "%s not added to B pipe,\n\n"
                            "direct and indirect layers used." % (lg)
                    )
                    skip_bpipe = True

            elif 'albedo' in lg_lower or 'color' in lg_lower or 'colour' in lg_lower or lg_lower == 'c':
                sticky_label = (
                    "%s not added to B pipe,\n\n"
                    "This AOV will break the basic rebuild.\n\n"
                    "Please use as needed"
                ) % (lg)
                skip_bpipe = True

        ## universal guards (apply to both materials and lightgroups)
        if not skip_bpipe and (lg_lower in ("ao", "gi") or "raw" in lg_lower or "filter" in lg_lower or "shadow" in lg_lower):
            sticky_label = (
                    "%s not added to B pipe,\n\n"
                    "This AOV will break the basic rebuild.\n\n"
                    "Please use as needed"
            ) % (lg)
            skip_bpipe = True

        if skip_bpipe:
            sticky_note = nuke.nodes.StickyNote(
                label=sticky_label,
                tile_color=0x272727ff,
                note_font_color=0xa8a8a8ff,
                note_font_size=11,
            )
            ## place the sticky note neatly above the shuffle node
            set_centred_xypos(sticky_note, int(x_pos), y_pos + 56)

        ## b-pipe connection
        if not skip_bpipe:
            ## only add to the valid list if the guard didn't trigger
            valid_aovs_for_unassigned.append(lg)

            x_pos -= (x_space * x_dir) * 0.5
            if first_merge:
                merge_inputs = [start_dot, aov_pipe[-1]]
                first_merge = False
            else:
                merge_inputs = [bpipe_nodes[-1], aov_pipe[-1]]

            merge_from = nuke.nodes.Merge2(inputs=merge_inputs, operation='from', output='rgb', tile_color=MERGE_FROM_COLOUR)
            set_centred_xypos(merge_from, int(x_pos), y_pos)
            bpipe_nodes.append(merge_from)

            x_pos += (x_space * x_dir) * 0.5
            y_pos += y_space * 2
            bottom_aov_dot = nuke.nodes.Dot(inputs=[aov_pipe[-1]])
            #bottom_aov_dot.setName('bottom_aov_dot', True) ## keep on? (check this)
            #bottom_aov_dot['label'].setValue('bottom_aov_dot')  ## debug layout
            set_centred_xypos(bottom_aov_dot, int(x_pos), y_pos)
            aov_pipe.append(bottom_aov_dot)

            x_pos -= (x_space * x_dir) * 0.5
            merge_plus = nuke.nodes.Merge2(inputs=[bpipe_nodes[-1], aov_pipe[-1]], operation='plus', output='rgb', tile_color=MERGE_PLUS_COLOUR)
            set_centred_xypos(merge_plus, int(x_pos), y_pos)
            bpipe_nodes.append(merge_plus)
        else:
            ## if skipped, add dot so the side pipe doesn't end. no merge nodes are created, leaving the B-pipe unaffected.
            y_pos += y_space * 2
            bottom_aov_dot = nuke.nodes.Dot(inputs=[aov_pipe[-1]])
            #bottom_aov_dot.setName('bottom_aov_dot', True) ## debug
            #bottom_aov_dot['label'].setValue('bottom_aov_dot')  ## debug layout
            set_centred_xypos(bottom_aov_dot, int(x_pos), y_pos)
            aov_pipe.append(bottom_aov_dot)

        ## ensure bpipe_xpos/ypos is updated for the next iteration (even if skipped)
        bpipe_xpos, bpipe_ypos = get_centre_xypos(bpipe_nodes[-1])

    last_aov_dot = entry_nodes[-1]

    ## unassigned pipe
    unassigned_pipe = []
    unassigned_x_pos, unassigned_y_pos = get_centre_xypos(start_aov_dot)
    unassigned_x_pos += (x_space * x_dir)
    if upstream_unassigned_dot:
        unassigned_aov_dot = nuke.nodes.Dot(inputs=[upstream_unassigned_dot])
    else:
        unassigned_aov_dot = nuke.nodes.Dot(inputs=[start_aov_dot])
    ## apply suffix to the name
    unassigned_aov_dot.setName('unassigned_aov_dot' + pipe_suffix, True)
    #unassigned_aov_dot['label'].setValue('unassigned_aov_dot' + pipe_suffix) ## debug layout
    set_centred_xypos(unassigned_aov_dot, unassigned_x_pos, unassigned_y_pos)
    entry_nodes.append(unassigned_aov_dot)
    unassigned_pipe.append(unassigned_aov_dot)

    y_pos += y_space
    unassigned_mat_dot = nuke.nodes.Dot(inputs=[unassigned_aov_dot])
    #unassigned_mat_dot['label'].setValue('unassigned_mat_dot') ## debug layout
    un_mat_x_pos, un_mat_y_pos = get_centre_xypos(unassigned_aov_dot)
    un_mat_y_pos += y_space * 2
    set_centred_xypos(unassigned_mat_dot, un_mat_x_pos, un_mat_y_pos)
    unassigned_pipe.append(unassigned_mat_dot)

    ## shift the x position by half a space before the loop begins
    unassigned_x_pos -= (x_space * x_dir) * 0.5
    unassigned_y_pos += y_space

    for lg in lightgroups_or_materials:
        unassigned_y_pos += y_space
        bpipe_ypos += y_space * 0.5
        merge_from = nuke.nodes.Merge2(inputs=[unassigned_pipe[-1], unassigned_pipe[-1]], Achannels=lg, operation='from', output='rgb', tile_color=MERGE_FROM_COLOUR, label=lg)
        set_centred_xypos(merge_from, int(unassigned_x_pos), int(unassigned_y_pos))
        unassigned_pipe.append(merge_from)

        y_pos += y_space

    ## qc check
    run_qc = False
    ct = None  ## initialize so it exists even if QC is skipped
    if mode == 0 and settings.get('check_unassigned_values_mats'):
        run_qc = True
        qc_name = "Check_Values_Materials\n\nMin Luma Pix Value: [value minlumapixvalue]"
    elif mode == 1 and settings.get('check_unassigned_values_lights'):
        run_qc = True
        qc_name = "Check_Values_Lightgroups\n\nMin Luma Pix Value: [value minlumapixvalue]"

    if run_qc:
        ct = nuke.nodes.CurveTool(inputs=[unassigned_pipe[-1]], note_font_color = 0xFFFFFFFF, note_font = 'bold')
        #ct.setName(qc_name, True) ## debug
        ct['label'].setValue(qc_name)
        ct['operation'].setValue('Max Luma Pixel')

        w, h = ct.input(0).width(), ct.input(0).height()
        ct['ROI'].setValue([0, 0, w, h])
        ct['ROI'].clearAnimated()

        unassigned_y_pos += y_space
        set_centred_xypos(ct, int(unassigned_x_pos), int(unassigned_y_pos))

        nuke.execute(ct, int(nuke.root()['first_frame'].value()), int(nuke.root()['last_frame'].value()))
        unassigned_pipe.append(ct)

    unassigned_bottom_vis_dot = nuke.nodes.Dot(inputs=[unassigned_pipe[-1]])
    unassigned_bottom_vis_dot.setName('unassigned_bottom_vis_dot', True)
    unassigned_bottom_vis_dot['label'].setValue('For Vis Only')
    unassigned_bottom_vis_dot["note_font_color"].setValue(int(0xFFFFFFFF))
    unassigned_bottom_vis_dot["note_font"].setValue("bold")
    unassigned_bottom_vis_dot["note_font_size"].setValue(40)
    set_centred_xypos(unassigned_bottom_vis_dot, int(unassigned_x_pos), int(unassigned_y_pos + y_space))

    ## add a custom tab and message to explain why the pipe ends here
    vis_tab = nuke.Tab_Knob('vis_info_tab', 'Vis Info')
    unassigned_bottom_vis_dot.addKnob(vis_tab)
    vis_msg = nuke.Text_Knob('vis_msg', '', 'The subtractive rebuild keeps unassigned AOVs so this pipe is for visualisation purposes only.')
    unassigned_bottom_vis_dot.addKnob(vis_msg)

    if run_qc and ct:
        analysis_results = ct['minlumapixvalue'].value()
        has_negatives = any(v < 0 for v in analysis_results)

        if has_negatives:
            ## red / disconnect
            ct['tile_color'].setValue(MERGE_FROM_COLOUR)
            #unassigned_bottom_vis_dot.setInput(0, None)  ## disconnect unassigned_bottom_vis_dot
            msg = "<font color=#eb4c34><b>Negative Values</b></font>\nUnassigned pipe disconnected. Negative values should not be plussed to the B pipe"
            sn = nuke.nodes.StickyNote(label=msg, tile_color=0x272727ff, note_font_color=0xa8a8a8ff, note_font_size=20)
            sn.setXYpos(int(unassigned_x_pos + (x_space * x_dir) * 3.2), int(unassigned_y_pos - 28))
        else:
            ## green / stay connected
            ct['tile_color'].setValue(MERGE_PLUS_COLOUR)
            msg = "<font color=#70EE70><b>Positive Values</b></font>\nUnassigned pipe may be plussed to the B pipe."
            sn = nuke.nodes.StickyNote(label=msg, tile_color=0x272727ff, note_font_color=0xa8a8a8ff, note_font_size=20)
            sn.setXYpos(int(unassigned_x_pos + (x_space * x_dir) * 2.1), int(unassigned_y_pos - 28))

    ## append the dot to the final list for the return
    unassigned_pipe.append(unassigned_bottom_vis_dot)

    return bpipe_nodes, last_aov_dot, unassigned_mat_dot

def subtractive_breakout_lightgroups_and_materials(node, settings=DEFAULT_SETTINGS):
    '''Runs a breakout of materials and lightgroups using subtractive logic.'''
    breakout_utilities_enabled = settings.get('breakout_utilities', False)

    ## breakout settings
    print(settings)
    breakout_materials = settings['breakout_materials']
    breakout_lightgroups = settings['breakout_lightgroups']
    expected_materials = settings['expected_materials']
    expected_utilities = settings['expected_utilities']
    lightgroup_regex = settings['lg_regex']
    additional_lighting = settings['additional_lighting']
    x_space = settings['x_space']
    x_dir = settings.get('x_dir', -1)
    y_space = settings['y_space']

    ## if there are no materials / lightgroups, run utilities only (if any)
    materials  = get_materials(node, expected_materials)
    ## respect user-edited list; otherwise exclude anything already classed as a material
    if settings.get('custom_lightgroups') is not None:
        lightgroups = settings['custom_lightgroups']
    else:
        lightgroups = get_lightgroup_layers(
            node, lightgroup_regex, additional_lighting,
            exclude=settings.get('lg_exclude', [])
        )
    utilities  = get_utilities(node, expected_utilities)

    master_exclude = set(settings.get('omit_list', []) + settings.get('unassigned_list', []))
    materials = [m for m in materials if m not in master_exclude]
    lightgroups = [lg for lg in lightgroups if lg not in master_exclude]
    utilities = [u for u in utilities if u not in master_exclude]

    ## track utility objects globally
    utility_dot = None
    utility_rgba_node = None

    if breakout_utilities_enabled:
        utl_result = breakout_utilities(node, settings)
        ## only unpack if utilities were actually found and built
        if utl_result:
            utility_dot, utility_rgba_node = utl_result

    ## guard : utilities only mode / fallback
    if not materials and not lightgroups:
        return

    ## begin main bpipe
    bpipe_nodes = []
    x_pos, y_pos = get_centre_xypos(node)
    y_pos += y_space

    ## identify which utilities are in the stream
    utilities_to_remove = get_utilities(node, settings['expected_utilities'])

    ## filter out 'rgba' and 'alpha' so they are not removed
    filtered_utilities = [utl for utl in utilities_to_remove if utl not in ('rgba', 'alpha')]

    if filtered_utilities:
        ## do not connect inputs yet
        remove_utilities_grp = nuke.nodes.Group() ## (label='Remove Utilities')
        remove_utilities_grp.setName('Remove_Utilities', True)
        remove_utilities_grp["tile_color"].setValue(int(0x9e3c6300))
        remove_utilities_grp["note_font_color"].setValue(int(0xFFFFFFFF))
        remove_utilities_grp["note_font"].setValue("bold")
        set_centred_xypos(remove_utilities_grp, x_pos, y_pos)

        ## create and add the Tab_Knob
        user_tab = nuke.Tab_Knob('removed_list_tab', 'Removed List')
        remove_utilities_grp.addKnob(user_tab)

        ## format the list of removed utilities (joined by line breaks for a clean list)
        removed_layers_str = '\n'.join(filtered_utilities)

        ## create a Text_Knob to display the string (ideal for read-only information)
        removed_info_knob = nuke.Text_Knob('removed_layers_info', '', removed_layers_str)
        remove_utilities_grp.addKnob(removed_info_knob)

        with remove_utilities_grp:
            grp_input = nuke.nodes.Input()
            curr_node = grp_input
            ## create one remove node for each utility layer
            for utl in filtered_utilities:  ## use the filtered list here
                remove_node = nuke.nodes.Remove(inputs=[curr_node], operation='remove', channels=utl)
                remove_node["note_font_color"].setValue(int(0xFFFFFFFF))
                remove_node["note_font"].setValue("bold")

                curr_node = remove_node
            ## cap off the inside of the group
            nuke.nodes.Output(inputs=[curr_node])
        ## connect the external pipe
        remove_utilities_grp.setInput(0, node)
    else:
        ## fallback to standard NoOp if no utilities exist (or if only rgba/alpha were present)
        remove_utilities_grp = nuke.nodes.NoOp(inputs=[node])
        remove_utilities_grp.setName('spacer_no_op', True)
        set_centred_xypos(remove_utilities_grp, x_pos, y_pos)

    bpipe_nodes.append(remove_utilities_grp)
    y_pos += y_space

    ## get all layers in the stream to check for crypto
    all_stream_layers = get_all_layers(node)

    ## filter for any layers containing 'crypto' (case-insensitive)
    crypto_layers = [layer for layer in all_stream_layers if 'crypto' in layer.lower()]

    if crypto_layers:
        ## create a group to house the remove nodes cleanly
        remove_crypto_grp = nuke.nodes.Group()
        remove_crypto_grp.setName('Remove_Crypto', True)
        remove_crypto_grp["tile_color"].setValue(int(0x9e3c6300))
        remove_crypto_grp["note_font_color"].setValue(int(0xFFFFFFFF))
        remove_crypto_grp["note_font"].setValue("bold")
        set_centred_xypos(remove_crypto_grp, x_pos, y_pos)

        ## create and add the Tab_Knob
        crypto_tab = nuke.Tab_Knob('crypto_list_tab', 'Crypto List')
        remove_crypto_grp.addKnob(crypto_tab)

        ## format the list of removed crypto layers (joined by line breaks)
        crypto_layers_str = '\n'.join(crypto_layers)

        ## create a Text_Knob to display the string
        crypto_info_knob = nuke.Text_Knob('crypto_layers_info', '', crypto_layers_str)
        remove_crypto_grp.addKnob(crypto_info_knob)

        with remove_crypto_grp:
            grp_input = nuke.nodes.Input()
            curr_node = grp_input

            ## create one remove node for each crypto layer
            for c_layer in crypto_layers:
                remove_node = nuke.nodes.Remove(inputs=[curr_node], operation='remove', channels=c_layer)
                remove_node["note_font_color"].setValue(int(0xFFFFFFFF))
                remove_node["note_font"].setValue("bold")

                curr_node = remove_node

            ## cap off the inside of the group
            nuke.nodes.Output(inputs=[curr_node])

        ## connect the external pipe to the last node in the bpipe
        remove_crypto_grp.setInput(0, bpipe_nodes[-1])
        bpipe_nodes.append(remove_crypto_grp)
        y_pos += y_space

    unpremult_aov = nuke.nodes.Unpremult(inputs=[bpipe_nodes[-1]], channels='all')
    unpremult_aov.setName('unpremult_aov', True)
    set_centred_xypos(unpremult_aov, x_pos, y_pos)
    bpipe_nodes.append(unpremult_aov)

    y_pos += y_space
    original_dot = nuke.nodes.Dot(inputs=[unpremult_aov])
    #original_dot['label'].setValue('original_dot') ## debug layout
    set_centred_xypos(original_dot, x_pos, y_pos)
    bpipe_nodes.append(original_dot)

    ## establish main pipeline position and original stream position
    main_x_pos = x_pos

    x_pos += (x_space * x_dir)
    divide_top_dot = nuke.nodes.Dot(inputs=[original_dot])
    #divide_top_dot['label'].setValue('divide_top_dot') ## debug layout
    set_centred_xypos(divide_top_dot, x_pos, y_pos)

    current_bpipe_end = original_dot
    original_pipe_end = divide_top_dot

    ## track the side-pipe tail dots globally
    last_mat_aov_dot = None
    last_mat_unassigned_dot = None

    ## materials breakout
    if breakout_materials == True and materials:
        ## unpack the tuple to catch the tail dots
        mat_pipe, last_mat_aov_dot, last_mat_unassigned_dot = subtractive_lightgroups_or_materials(divide_top_dot, 0, settings)
        bpipe_nodes.extend(mat_pipe)

        mat_end_x, mat_end_y = get_centre_xypos(mat_pipe[-1])
        y_pos = mat_end_y + y_space
        divide_mat_dot = nuke.nodes.Dot(inputs=[original_pipe_end])
        set_centred_xypos(divide_mat_dot, x_pos, y_pos)
        #divide_mat_dot['label'].setValue('divide_mat_dot') ## debug layout
        original_pipe_end = divide_mat_dot

        merge_divide_mat = nuke.nodes.Merge2(inputs=[original_pipe_end, mat_pipe[-1]], operation='divide', output='rgb')
        set_centred_xypos(merge_divide_mat, mat_end_x, y_pos)
        bpipe_nodes.append(merge_divide_mat)

        y_pos += y_space
        divide_dot_mat = nuke.nodes.Dot(inputs=[merge_divide_mat])
        #divide_dot_mat['label'].setValue('divide_dot_mat') ## debug layout
        set_centred_xypos(divide_dot_mat, mat_end_x, y_pos)

        merge_multiply_mat = nuke.nodes.Merge2(inputs=[current_bpipe_end, divide_dot_mat], operation='multiply', output='rgb')
        set_centred_xypos(merge_multiply_mat, main_x_pos, y_pos)
        bpipe_nodes.append(merge_multiply_mat)

        y_pos += y_space * 2
        spacer_dot = nuke.nodes.Dot(inputs=[merge_multiply_mat])
        spacer_dot.setName('spacer_dot', True)
        #spacer_dot['label'].setValue('spacer_dot')  ## debug layout
        set_centred_xypos(spacer_dot, main_x_pos, y_pos)
        bpipe_nodes.append(spacer_dot)

        current_bpipe_end = spacer_dot

    # elif breakout_materials == True:
    #     sticky_label = '<h3>Missing Materials</h3>There are no materials in this stream.'
    #     sticky_note = nuke.nodes.StickyNote(
    #         label=sticky_label,
    #         tile_color=0x272727ff,
    #         note_font_color=0xa8a8a8ff,
    #         note_font_size=40
    #     )
    #     sticky_note.setXYpos(int(main_x_pos + (x_space * x_dir) * 7), int(y_pos))

    ## lightgroups breakout
    if breakout_lightgroups == True and lightgroups:
        lg_start_input = current_bpipe_end if last_mat_aov_dot is not None else divide_top_dot
        ## use original_pipe_end for layout X position (-x_space offset), but pass current_bpipe_end as the start_input to connect to spacer_dot
        lg_pipe, _, _ = subtractive_lightgroups_or_materials(original_pipe_end, 1, settings, start_input=lg_start_input, upstream_aov_dot=last_mat_aov_dot, upstream_unassigned_dot=last_mat_unassigned_dot)
        bpipe_nodes.extend(lg_pipe)

        lg_end_x, lg_end_y = get_centre_xypos(lg_pipe[-1])
        y_pos = lg_end_y + y_space
        divide_lg_dot = nuke.nodes.Dot(inputs=[original_pipe_end])
        #divide_lg_dot['label'].setValue('divide_lg_dot') ## debug layout
        set_centred_xypos(divide_lg_dot, x_pos, y_pos)
        original_pipe_end = divide_lg_dot

        merge_divide_lg = nuke.nodes.Merge2(inputs=[original_pipe_end, lg_pipe[-1]], operation='divide', output='rgb')
        set_centred_xypos(merge_divide_lg, lg_end_x, y_pos)
        bpipe_nodes.append(merge_divide_lg)

        y_pos += y_space
        divide_dot_lg = nuke.nodes.Dot(inputs=[merge_divide_lg])
        #divide_dot_lg['label'].setValue('divide_dot_lg') ## debug layout
        set_centred_xypos(divide_dot_lg, lg_end_x, y_pos)

        merge_multiply_lg = nuke.nodes.Merge2(inputs=[current_bpipe_end, divide_dot_lg], operation='multiply',
                                              output='rgb')
        set_centred_xypos(merge_multiply_lg, main_x_pos, y_pos)
        bpipe_nodes.append(merge_multiply_lg)

        y_pos += y_space
        lg_dot_bottom = nuke.nodes.Dot(inputs=[merge_multiply_lg])
        lg_dot_bottom.setName('lg_dot_bottom', True)
        #lg_dot_bottom['label'].setValue('lg_dot_bottom') ## debug layout
        set_centred_xypos(lg_dot_bottom, main_x_pos, y_pos)
        bpipe_nodes.append(lg_dot_bottom)
        current_bpipe_end = lg_dot_bottom

    ## feedback to artist on missing lightgroup AOVs
    # elif breakout_lightgroups == True:
    #     sticky_label = '<h3>Missing Lightgroups</h3>There are no lightgroups in this stream (as per the regex).'
    #     sticky_note = nuke.nodes.StickyNote(
    #         label=sticky_label,
    #         tile_color=0x272727ff,
    #         note_font_color=0xa8a8a8ff,
    #         note_font_size=40
    #     )
    #     sticky_note.setXYpos(int(main_x_pos + (x_space * x_dir) * 9), int(y_pos))
    #     y_pos += y_space

    ## create a bypass dot if utilities are unchecked
    if not breakout_utilities_enabled:
        node_x, node_y = get_centre_xypos(node)

        keep_rgba = nuke.nodes.Remove(inputs=[node], label='rgba', note_font_color=0xFFFFFFFF, note_font='bold', operation='keep', channels='rgba')
        set_centred_xypos(keep_rgba, int(node_x + (x_space * x_dir)), node_y)

        bypass_dot = nuke.nodes.Dot(inputs=[keep_rgba])
        #bypass_dot['label'].setValue('bypass_dot') ## debug layout
        set_centred_xypos(bypass_dot, int(node_x + (x_space * x_dir) * 5), node_y)

        original_rgba_source = bypass_dot
    else:
        ## if the utility shuffle was created, use it. otherwise fallback to the top of the B-pipe
        original_rgba_source = utility_rgba_node if utility_rgba_node else bpipe_nodes[0]

    ## get the x position of original_rgba_source to align the vertical pipe
    rgba_source_x, _ = get_centre_xypos(original_rgba_source)

    y_pos += y_space * 2
    ## create a Dot for the Switch node
    switch_dot = nuke.nodes.Dot(inputs=[original_rgba_source])
    switch_dot.setName('switch_dot', True)
    # switch_dot['label'].setValue('switch_dot') ## debug layout
    set_centred_xypos(switch_dot, rgba_source_x, y_pos)

    ## dynamically fetch the B-pipe's end position for alignment
    bpipe_x, _ = get_centre_xypos(current_bpipe_end)

    ## compensate for the post_layout_adjustments script shifting downstream nodes based on reflection
    tail_x_pos = int(bpipe_x - ((x_space * x_dir) * 2 if breakout_utilities_enabled else 0))

    ## unpremult the original stream for an accurate A/B comparison. shifted horizontally to create a clean corner
    unpremult_x = int(tail_x_pos + (x_space * x_dir))
    switch_unpremult = nuke.nodes.Unpremult(inputs=[switch_dot])
    set_centred_xypos(switch_unpremult, unpremult_x, y_pos)

    ## create a Switch node for A/B comparison
    compare_switch = nuke.nodes.Switch(inputs=[current_bpipe_end, switch_unpremult], label='Compare Beauty')
    compare_switch["note_font_color"].setValue(int(0xFFFFFFFF))
    compare_switch["note_font"].setValue("bold")
    set_centred_xypos(compare_switch, tail_x_pos, y_pos)
    bpipe_nodes.append(compare_switch)

    y_pos += y_space
    ## create a Dot for the Copy node
    copy_dot = nuke.nodes.Dot(inputs=[switch_dot])
    copy_dot.setName('copy_dot', True)
    # copy_dot['label'].setValue('copy_dot') ## debug layout
    set_centred_xypos(copy_dot, rgba_source_x, y_pos)

    ## copy the original alpha back into the rebuilt stream
    copy_alpha = nuke.nodes.Copy(inputs=[bpipe_nodes[-1], copy_dot], from0='rgba.alpha', to0='rgba.alpha')
    set_centred_xypos(copy_alpha, tail_x_pos, y_pos)
    bpipe_nodes.append(copy_alpha)

    final_premult = nuke.nodes.Premult(inputs=[bpipe_nodes[-1]])
    set_centred_xypos(final_premult, tail_x_pos, y_pos + 32)
    bpipe_nodes.append(final_premult)

    keep_rgba = nuke.nodes.Remove(inputs=[bpipe_nodes[-1]], operation='keep', channels='rgba')
    set_centred_xypos(keep_rgba, tail_x_pos, y_pos + 58)
    bpipe_nodes.append(keep_rgba)

    return bpipe_nodes

def subtractive_post_layout_adjustments(x_space, x_dir=-1):
    '''Deletes placeholder nodes not relevant to the network and adjusts utility layout.'''
    deleted_NoOps = 0

    ## delete NoOps
    for n in nuke.allNodes('NoOp'):
        if 'spacer_no_op' in n.name():
            nuke.delete(n)
            deleted_NoOps += 1

    ## Determine which streams were built
    mat_ran = any('start_dot_mat' in n.name() for n in nuke.allNodes('Dot'))
    lg_ran = any('start_dot_lg' in n.name() for n in nuke.allNodes('Dot'))

    ## If ONLY materials ran, delete spacer_dot
    if mat_ran and not lg_ran:
        for n in nuke.allNodes('Dot'):
            if 'spacer_dot' in n.name():
                nuke.delete(n)

    ## delete lg_dot_bottom dot
    for n in nuke.allNodes('Dot'):
        if 'lg_dot_bottom' in n.name():
            nuke.delete(n)

    ## Delete redundant top routing dots for lightgroups if materials ran
    if mat_ran:
        redundant_lg_dots = ['unassigned_aov_dot_lg', 'start_aov_dot_lg', 'start_dot_lg']
        for n in nuke.allNodes('Dot'):
            if any(dot_name in n.name() for dot_name in redundant_lg_dots):
                nuke.delete(n)

    ## offset utility breakout nodes systematically in the correct direction
    utility_roots = [n for n in nuke.allNodes('Dot') if
                     n.knob('label') and str(n['label'].value()).startswith('< UTILITY')]

    for utility_root in utility_roots:
        nodes_to_move = set()

        # Recursively collect all downstream nodes generated in the utility breakout
        def collect_downstream(current_node):
            for dep in current_node.dependent():
                if dep not in nodes_to_move:
                    nodes_to_move.add(dep)
                    collect_downstream(dep)

        collect_downstream(utility_root)

        offset = int(x_space * 2 * x_dir)
        for n in nodes_to_move:
            n.setXpos(int(n.xpos() + offset))

    print("post_layout_adjustments() ran:",
          "deleted_NoOps =", deleted_NoOps)