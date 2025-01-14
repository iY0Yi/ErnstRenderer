// Climbers and Watchers have 16 poses each.
// It's like a sprite sheet on NES :)

// TRV is variables for Transformation.
#define TRVS_NUM @BL_TRVS_NUM
@BL_TRVS_DEF
int TRVsID = 0;
#define IS_EDITING_TRVS @BL_IS_EDITING_TRVS

// Lists of no overwrapped random ids.
// here is the list generator:
// https://codepen.io/iy0yi/pen/qBXoGBp?editors=0011

#define IDS_ALL_TABLE_NUM 160
const int[IDS_ALL_TABLE_NUM] ids_All = int[](10,15,14,8,3,2,6,7,13,12,5,11,1,9,4,0,12,9,13,11,1,5,10,7,14,0,8,6,3,15,4,2,15,10,14,0,4,12,11,7,9,13,2,1,3,6,8,5,1,5,2,10,4,15,6,12,11,0,14,9,8,7,3,13,8,3,9,0,12,4,2,7,13,11,6,10,5,15,14,1,12,14,9,13,11,0,15,6,7,3,10,2,4,1,5,8,14,1,11,8,15,0,5,6,10,4,7,13,12,3,9,2,1,14,2,0,13,12,10,5,9,15,8,4,11,6,7,3,13,2,10,3,1,8,12,5,0,7,14,15,9,11,6,4,13,2,12,4,7,1,6,10,11,9,15,14,3,8,0,5); // 0-15

#define TRVS_ID_C_DEFAULT 0
#define TRVS_ID_C_OFFSETED 1
#define TRVS_ID_C_PATIENT 2
#define TRVS_ID_C_PATIENT_FALLING 3
#define TRVS_ID_C_FALLING 4
#define IDS_C_DEFALUT_TABLE_NUM 110
const int[IDS_C_DEFALUT_TABLE_NUM] ids_C_Default = int[](7,3,6,1,5,8,4,0,10,9,3,4,5,0,8,7,1,3,2,6,10,9,10,4,7,1,0,3,2,9,8,6,5,4,3,6,9,7,2,8,1,10,0,5,0,7,2,4,2,5,6,8,1,9,10,0,8,4,6,5,10,2,1,3,9,7,5,4,3,9,8,2,7,0,10,6,1,0,6,10,5,4,1,3,7,8,2,9,8,6,9,3,2,0,7,10,5,1,4,2,1,0,10,8,9,7,6,4,5,3); // 0-10
#define IDS_C_OFFSETED_TABLE_NUM 60
const int[IDS_C_OFFSETED_TABLE_NUM] ids_C_Offseted = int[](2,5,0,1,4,3,4,2,3,5,2,0,4,2,3,0,1,5,4,2,5,3,4,0,2,1,0,5,4,3,1,2,5,5,0,4,1,5,0,2,4,3,2,0,4,3,1,5,2,1,0,4,3,5,2,3,5,1,0,4); // 0-5
#define IDS_C_PATIENT_TABLE_NUM 30
const int[IDS_C_PATIENT_TABLE_NUM] ids_C_Patient = int[](12,13,11,12,13,11,13,11,12,11,12,13,11,12,13,11,13,12,11,13,12,11,13,12,13,11,12,13,11,12); // 11-13
#define IDS_C_PATIENT_FALLING_TABLE_NUM 50
const int[IDS_C_PATIENT_FALLING_TABLE_NUM] ids_C_Patient_Falling = int[](12,15,13,11,14,13,12,14,11,15,11,13,15,12,14,13,14,11,12,15,14,12,11,15,13,15,14,12,11,13,12,11,14,13,15,12,15,11,14,13,14,11,15,12,13,14,11,12,15,13); // 11-15
#define IDS_C_FALLING_TABLE_NUM 10
const int[IDS_C_FALLING_TABLE_NUM] ids_C_Falling = int[](14,15,14,15,14,15,14,15,14,15); // 14-15

#define TRVS_ID_W_LIFTING 5
#define TRVS_ID_W_CARRYING 6
#define TRVS_ID_W_OPENNING 7
#define TRVS_ID_W_CLOSED 8
#define TRVS_ID_W_PEEPING 9
#define TRVS_ID_W_DROPPING 10
#define TRVS_ID_W_VIEWING 11
#define TRVS_ID_W_GENERAL 12
#define IDS_W_LIFTING_TABLE_NUM 1
const int[IDS_W_LIFTING_TABLE_NUM] ids_W_Lifting = int[](0); // 0
#define IDS_W_CARRYING_TABLE_NUM 10
const int[IDS_W_CARRYING_TABLE_NUM] ids_W_Carrying = int[](2,1,1,2,1,2,1,2,2,1); // 1-2
#define IDS_W_OPENNING_TABLE_NUM 15
const int[IDS_W_OPENNING_TABLE_NUM] ids_W_Openning = int[](4,3,5,3,5,4,3,4,5,4,5,3,5,3,4); // 3-5
#define IDS_W_CLOSED_TABLE_NUM 1
const int[IDS_W_CLOSED_TABLE_NUM] ids_W_Closed = int[](6); // 6
#define IDS_W_PEEPING_TABLE_NUM 15
const int[IDS_W_PEEPING_TABLE_NUM] ids_W_Peeping = int[](8,7,9,8,9,7,9,8,7,7,9,8,8,9,7); // 7-9
#define IDS_W_DROPPING_TABLE_NUM 10
const int[IDS_W_DROPPING_TABLE_NUM] ids_W_Dropping = int[](10,11,10,11,10,11,10,11,11,10); // 10-11
#define IDS_W_VIEWING_TABLE_NUM 15
const int[IDS_W_VIEWING_TABLE_NUM] ids_W_Viewing = int[](12,14,13,12,14,13,13,14,12,13,12,14,14,12,13); // 12-14
#define IDS_W_GENERAL_TABLE_NUM 1
const int[IDS_W_GENERAL_TABLE_NUM] ids_W_General = int[](15); // 15

int getId(float pid, int idType) {
    switch(idType){
        case TRVS_ID_C_DEFAULT:
            return ids_C_Default[int(IDS_C_DEFALUT_TABLE_NUM-1-int(mod(pid, float(IDS_C_DEFALUT_TABLE_NUM))))];
        case TRVS_ID_C_OFFSETED:
            return ids_C_Offseted[int(IDS_C_OFFSETED_TABLE_NUM-1-int(mod(pid, float(IDS_C_OFFSETED_TABLE_NUM))))];
        case TRVS_ID_C_PATIENT:
            return ids_C_Patient[int(IDS_C_PATIENT_TABLE_NUM-1-int(mod(pid, float(IDS_C_PATIENT_TABLE_NUM))))];
        case TRVS_ID_C_PATIENT_FALLING:
            return ids_C_Patient_Falling[int(IDS_C_PATIENT_FALLING_TABLE_NUM-1-int(mod(pid, float(IDS_C_PATIENT_FALLING_TABLE_NUM))))];
        case TRVS_ID_C_FALLING:
            return ids_C_Falling[int(IDS_C_FALLING_TABLE_NUM-1-int(mod(pid, float(IDS_C_FALLING_TABLE_NUM))))];
        case TRVS_ID_W_LIFTING:
            return ids_W_Lifting[int(IDS_W_LIFTING_TABLE_NUM-1-int(mod(pid, float(IDS_W_LIFTING_TABLE_NUM))))];
        case TRVS_ID_W_CARRYING:
            return ids_W_Carrying[int(IDS_W_CARRYING_TABLE_NUM-1-int(mod(pid, float(IDS_W_CARRYING_TABLE_NUM))))];
        case TRVS_ID_W_OPENNING:
            return ids_W_Openning[int(IDS_W_OPENNING_TABLE_NUM-1-int(mod(pid, float(IDS_W_OPENNING_TABLE_NUM))))];
        case TRVS_ID_W_CLOSED:
            return ids_W_Closed[int(IDS_W_CLOSED_TABLE_NUM-1-int(mod(pid, float(IDS_W_CLOSED_TABLE_NUM))))];
        case TRVS_ID_W_PEEPING:
            return ids_W_Peeping[int(IDS_W_PEEPING_TABLE_NUM-1-int(mod(pid, float(IDS_W_PEEPING_TABLE_NUM))))];
        case TRVS_ID_W_DROPPING:
            return ids_W_Dropping[int(IDS_W_DROPPING_TABLE_NUM-1-int(mod(pid, float(IDS_W_DROPPING_TABLE_NUM))))];
        case TRVS_ID_W_VIEWING:
            return ids_W_Viewing[int(IDS_W_VIEWING_TABLE_NUM-1-int(mod(pid, float(IDS_W_VIEWING_TABLE_NUM))))];
        case TRVS_ID_W_GENERAL:
            return ids_W_General[int(IDS_W_GENERAL_TABLE_NUM-1-int(mod(pid, float(IDS_W_GENERAL_TABLE_NUM))))];
        default:
            return ids_All[int(mod(pid, float(IDS_ALL_TABLE_NUM-1)))];
    }
}
