import { Moment } from 'moment'

export default interface Alarm {
    id?: number,
    time: Moment,
    label: string,
    enabled: boolean,
    repeat: boolean,
    repeat_sunday: boolean,
    repeat_monday: boolean,
    repeat_tuesday: boolean,
    repeat_wednesday: boolean,
    repeat_thursday: boolean,
    repeat_friday: boolean,
    repeat_saturday: boolean
}