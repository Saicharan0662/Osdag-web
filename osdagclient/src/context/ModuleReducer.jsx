
/* 
    ######################################################### 
    # Author : Atharva Pingale ( FOSSEE Summer Fellow '23 ) # 
    ######################################################### 
*/

export default (state, action) => {
    switch (action.type) {
        case 'SET_CONNECTIVITY_LIST' : 
            return {
                ...state , 
                connectivityList : action.payload,
                error_msg : 'Error in fetching Connectivity List'
            }
        case 'SET_COLUMN_BEAM_MATERIAL_LIST' : 
            return{
                ...state , 
                columnList : action.payload.columnList,
                beamList : action.payload.beamList,
                materialList : action.payload.materialList,
                error_msg : 'Error in fetching Column, Beam and Material List'
            }
        case 'SET_BEAM_MATERIAL_LIST' :
            return{
                ...state ,
                beamList : action.payload.beamList,
                materialList : action.payload.materialList,
                error_msg : 'Error in fetching Beam and Material List'
            }
        case 'SET_COOKIE_FETCH' : 
            return{
                ...state,
                setTheCookie : !state.setTheCookie
            }
        
        case 'SET_BOLT_DIAMETER_LIST' : 
            return{
                ...state,
                boltDiameterList : action.payload.boltList
            }
           
        case 'SET_THICKNESS_LIST' : 
            return{
                ...state,
                thicknessList : action.payload.thicknessList
            }
        
        case 'SET_PROPERTY_CLASS_LIST' : 
            return{
                ...state,
                propertyClassList : action.payload.propertyClassList
            }
        case 'SET_DESIGN_DATA_AND_LOGS' :   
            return{
                ...state,
                designData : action.payload.data,
                designLogs : action.payload.logs
            }

        case 'SET_RENDER_CAD_MODEL_BOOLEAN' : 
            return{
                ...state,
                renderCadModel : action.payload
            }
        case 'SET_REPORT_ID_AND_DISPLAY_PDF' : 
            return{
                ...state,
                report_id : action.payload,
                displayPDF : true
            }
        case 'SET_BLOBL_URL' : 
            return{
                ...state,
                blobUrl : action.payload
            }

        default:
            return state;
    }
}