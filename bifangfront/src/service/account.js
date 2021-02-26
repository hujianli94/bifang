import {request,METHOD} from '@/utils/request'
import {urlFormat} from '@/utils/util'
import {API} from './api'

/**
 * 获取账户组列表
 * @param {*} params 
 */
async function GroupList(params){

    return request(
        API.GROUPLIST, 
        METHOD.GET,
        params
    )
}

/**
 * 新增账户组
 * @param {*} params 
 */
async function CreateGroup(params){

    return request(
        API.CREATEGROUP, 
        METHOD.POST,
        params
    )
}

/**
 * 删除服务器
 * @param {*} params 
 */
async function DeleteGroup(params){
    const url = urlFormat(API.DELETEGROUP, params)
    return request(
        url, 
        METHOD.DELETE
    )
}

/**
 *更新服务器
 * @param {*} params 
 */
async function UpdateGroup(params){
    const url = urlFormat(API.UPDATEGROUP, params)
    return request(
        url, 
        METHOD.PUT,
        params
    )
}

/**
 * 获取账户组列表
 * @param {*} params 
 */
async function UserList(params){

    return request(
        API.USERLIST, 
        METHOD.GET,
        params
    )
}

/**
 * 新增账户组
 * @param {*} params 
 */
async function CreateUser(params){

    return request(
        API.CREATEUSER, 
        METHOD.POST,
        params
    )
}

/**
 * 删除服务器
 * @param {*} params 
 */
async function DeleteUser(params){
    const url = urlFormat(API.DELETEUSER, params)
    return request(
        url, 
        METHOD.DELETE
    )
}

/**
 *更新服务器
 * @param {*} params 
 */
async function UpdateUser(params){
    const url = urlFormat(API.UPDATEUSER, params)
    return request(
        url, 
        METHOD.PUT,
        params
    )
}

export default {
    GroupList,
    CreateGroup,
    UpdateGroup,
    DeleteGroup,
    UserList,
    CreateUser,
    UpdateUser,
    DeleteUser
}