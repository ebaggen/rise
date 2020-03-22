export default interface Alarm {
    id: number,
    time: Date,
    label: string,
    enabled: boolean,
    repeat: boolean,
    sunday_repeat: boolean,
    monday_repeat: boolean,
    tuesday_repeat: boolean,
    wednesday_repeat: boolean,
    thursday_repeat: boolean,
    friday_repeat: boolean,
    saturday_repeat: boolean
}